"""Backtesting Engine.

Implements the core backtesting logic using historical daily bars
to simulate rule-based strategies.
"""

from dataclasses import dataclass, field
from datetime import datetime

from asx_jobs.backtest.strategy import SignalType, Strategy, StrategySignal
from asx_jobs.database import Database
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class BacktestConfig:
    """Configuration for a backtest run.

    Attributes:
        start_date: Backtest start date (YYYY-MM-DD).
        end_date: Backtest end date (YYYY-MM-DD).
        initial_capital: Starting capital.
        position_size_pct: Position size as percentage of portfolio (0.0-1.0).
        max_positions: Maximum number of concurrent positions.
        commission_pct: Commission as percentage of trade value.
        slippage_pct: Slippage as percentage of price.
        universe: List of instrument IDs to trade, or None for all.
    """

    start_date: str
    end_date: str
    initial_capital: float = 100000.0
    position_size_pct: float = 0.1
    max_positions: int = 10
    commission_pct: float = 0.001
    slippage_pct: float = 0.001
    universe: list[int] | None = None


@dataclass
class Position:
    """Represents an open position.

    Attributes:
        instrument_id: Instrument database ID.
        symbol: Instrument ticker symbol.
        quantity: Number of shares held.
        entry_price: Average entry price.
        entry_date: Date position was opened.
        entry_value: Total value at entry (including commission).
    """

    instrument_id: int
    symbol: str
    quantity: int
    entry_price: float
    entry_date: str
    entry_value: float


@dataclass
class Trade:
    """Represents a completed trade.

    Attributes:
        instrument_id: Instrument database ID.
        symbol: Instrument ticker symbol.
        entry_date: Date position was opened.
        entry_price: Entry price.
        exit_date: Date position was closed.
        exit_price: Exit price.
        quantity: Number of shares.
        side: Trade side ("buy" for long).
        pnl: Profit/loss amount.
        pnl_percent: Profit/loss percentage.
        exit_reason: Reason for exiting.
        commission: Total commission paid.
    """

    instrument_id: int
    symbol: str
    entry_date: str
    entry_price: float
    exit_date: str
    exit_price: float
    quantity: int
    side: str
    pnl: float
    pnl_percent: float
    exit_reason: str | None
    commission: float


@dataclass
class BacktestMetrics:
    """Calculated metrics for a backtest run.

    Attributes:
        total_return: Total return as decimal (e.g., 0.15 = 15%).
        annualized_return: Annualized return as decimal.
        sharpe_ratio: Sharpe ratio (assuming 0% risk-free rate).
        sortino_ratio: Sortino ratio.
        max_drawdown: Maximum drawdown as decimal.
        max_drawdown_duration: Max drawdown duration in days.
        win_rate: Percentage of winning trades.
        profit_factor: Gross profit / gross loss.
        total_trades: Total number of trades.
        winning_trades: Number of winning trades.
        losing_trades: Number of losing trades.
        avg_win: Average winning trade amount.
        avg_loss: Average losing trade amount.
        largest_win: Largest single win.
        largest_loss: Largest single loss.
        avg_holding_period_days: Average holding period in days.
        exposure_time: Percentage of time with open positions.
    """

    total_return: float = 0.0
    annualized_return: float = 0.0
    sharpe_ratio: float | None = None
    sortino_ratio: float | None = None
    max_drawdown: float = 0.0
    max_drawdown_duration: int = 0
    win_rate: float = 0.0
    profit_factor: float | None = None
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    avg_win: float | None = None
    avg_loss: float | None = None
    largest_win: float | None = None
    largest_loss: float | None = None
    avg_holding_period_days: float | None = None
    exposure_time: float = 0.0


@dataclass
class BacktestResult:
    """Result of a backtest run.

    Attributes:
        run_id: Database ID of the backtest run.
        strategy_name: Name of the strategy.
        config: Backtest configuration.
        initial_capital: Starting capital.
        final_capital: Ending capital.
        metrics: Calculated performance metrics.
        trades: List of all trades executed.
        equity_curve: Daily equity values.
    """

    run_id: int
    strategy_name: str
    config: BacktestConfig
    initial_capital: float
    final_capital: float
    metrics: BacktestMetrics
    trades: list[Trade] = field(default_factory=list)
    equity_curve: list[tuple[str, float]] = field(default_factory=list)


class BacktestEngine:
    """Main backtesting engine.

    Simulates strategy execution using historical data.
    """

    def __init__(self, db: Database) -> None:
        """Initialize the engine.

        Args:
            db: Database client.
        """
        self.db = db

    def run(
        self,
        strategy: Strategy,
        config: BacktestConfig,
        run_name: str | None = None,
    ) -> BacktestResult:
        """Execute a backtest.

        Args:
            strategy: Trading strategy to test.
            config: Backtest configuration.
            run_name: Optional name for this run.

        Returns:
            BacktestResult with all metrics and trades.
        """
        logger.info(
            "backtest_started",
            strategy=strategy.name,
            start_date=config.start_date,
            end_date=config.end_date,
            initial_capital=config.initial_capital,
        )

        strategy_id = self.db.get_or_create_strategy(
            name=strategy.name,
            description=strategy.description,
            version=strategy.version,
            parameters=strategy.get_parameters(),
        )

        run_id = self.db.create_backtest_run(
            strategy_id=strategy_id,
            start_date=config.start_date,
            end_date=config.end_date,
            initial_capital=config.initial_capital,
            parameters=strategy.get_parameters(),
            name=run_name,
        )

        try:
            result = self._execute_backtest(strategy, config, run_id)

            self.db.complete_backtest_run(
                backtest_run_id=run_id,
                final_capital=result.final_capital,
                status="completed",
            )

            self._persist_trades(run_id, result.trades)
            self._persist_metrics(run_id, result.metrics)

            logger.info(
                "backtest_completed",
                run_id=run_id,
                total_return=f"{result.metrics.total_return:.2%}",
                total_trades=result.metrics.total_trades,
                win_rate=f"{result.metrics.win_rate:.2%}",
            )

            return result

        except Exception as e:
            logger.error("backtest_failed", run_id=run_id, error=str(e))
            self.db.complete_backtest_run(
                backtest_run_id=run_id,
                final_capital=config.initial_capital,
                status="failed",
                error_message=str(e),
            )
            raise

    def _execute_backtest(
        self,
        strategy: Strategy,
        config: BacktestConfig,
        run_id: int,
    ) -> BacktestResult:
        """Execute the backtest simulation.

        Args:
            strategy: Trading strategy.
            config: Backtest configuration.
            run_id: Database run ID.

        Returns:
            BacktestResult with simulation results.
        """
        if config.universe:
            instruments = [self.db.get_instrument_by_id(i) for i in config.universe]
            instruments = [i for i in instruments if i]
        else:
            instruments = self.db.get_all_active_instruments()

        instrument_ids = [i["id"] for i in instruments]
        symbol_map = {i["id"]: i["symbol"] for i in instruments}

        logger.info(
            "loading_price_data",
            instruments=len(instruments),
            start_date=config.start_date,
            end_date=config.end_date,
        )

        prices_by_instrument = self.db.get_all_price_history_range(
            start_date=config.start_date,
            end_date=config.end_date,
            instrument_ids=instrument_ids,
        )

        all_dates: set[str] = set()
        for prices in prices_by_instrument.values():
            for p in prices:
                all_dates.add(p["trade_date"])
        trading_days = sorted(all_dates)

        if not trading_days:
            raise ValueError("No trading days found in the specified date range")

        logger.info("simulation_starting", trading_days=len(trading_days))

        cash = config.initial_capital
        positions: dict[int, Position] = {}
        trades: list[Trade] = []
        equity_curve: list[tuple[str, float]] = []
        days_with_positions = 0

        strategy.on_start(config.start_date, config.end_date)

        for day_idx, trade_date in enumerate(trading_days):
            signals: list[StrategySignal] = []

            for inst_id in instrument_ids:
                if inst_id not in prices_by_instrument:
                    continue

                prices = prices_by_instrument[inst_id]
                bar_idx = next(
                    (i for i, p in enumerate(prices) if p["trade_date"] == trade_date),
                    None,
                )

                if bar_idx is None:
                    continue

                bar = prices[bar_idx]
                history = prices[:bar_idx]

                position_info = None
                if inst_id in positions:
                    pos = positions[inst_id]
                    current_price = bar["close"]
                    unrealized_pnl = (current_price - pos.entry_price) * pos.quantity
                    position_info = {
                        "quantity": pos.quantity,
                        "entry_price": pos.entry_price,
                        "entry_date": pos.entry_date,
                        "unrealized_pnl": unrealized_pnl,
                    }

                symbol = symbol_map[inst_id]
                signal = strategy.on_bar(inst_id, symbol, bar, history, position_info)

                if signal:
                    signals.append(signal)

            for signal in signals:
                inst_id = signal.instrument_id

                if signal.signal_type == SignalType.SELL:
                    if inst_id in positions:
                        trade, proceeds = self._close_position(
                            positions[inst_id],
                            signal.price,
                            trade_date,
                            signal.reason or "strategy_exit",
                            config,
                        )
                        trades.append(trade)
                        cash += proceeds
                        del positions[inst_id]

                elif signal.signal_type == SignalType.BUY:
                    if inst_id not in positions and len(positions) < config.max_positions:
                        position_value = config.initial_capital * config.position_size_pct
                        position_value = min(position_value, cash)

                        if position_value > 0:
                            position, cost = self._open_position(
                                inst_id,
                                signal.symbol,
                                signal.price,
                                trade_date,
                                position_value,
                                config,
                            )
                            if position:
                                positions[inst_id] = position
                                cash -= cost

            portfolio_value = cash
            for inst_id, pos in positions.items():
                if inst_id in prices_by_instrument:
                    prices = prices_by_instrument[inst_id]
                    bar = next(
                        (p for p in prices if p["trade_date"] == trade_date),
                        None,
                    )
                    if bar:
                        portfolio_value += bar["close"] * pos.quantity

            equity_curve.append((trade_date, portfolio_value))

            if positions:
                days_with_positions += 1

        for inst_id, pos in list(positions.items()):
            if inst_id in prices_by_instrument:
                prices = prices_by_instrument[inst_id]
                last_bar = next(
                    (p for p in reversed(prices) if p["trade_date"] <= config.end_date),
                    None,
                )
                if last_bar:
                    trade, proceeds = self._close_position(
                        pos,
                        last_bar["close"],
                        config.end_date,
                        "backtest_end",
                        config,
                    )
                    trades.append(trade)
                    cash += proceeds

        strategy.on_end()

        final_capital = cash
        metrics = self._calculate_metrics(
            trades,
            equity_curve,
            config.initial_capital,
            final_capital,
            len(trading_days),
            days_with_positions,
        )

        return BacktestResult(
            run_id=run_id,
            strategy_name=strategy.name,
            config=config,
            initial_capital=config.initial_capital,
            final_capital=final_capital,
            metrics=metrics,
            trades=trades,
            equity_curve=equity_curve,
        )

    def _open_position(
        self,
        instrument_id: int,
        symbol: str,
        price: float,
        date: str,
        target_value: float,
        config: BacktestConfig,
    ) -> tuple[Position | None, float]:
        """Open a new position.

        Args:
            instrument_id: Instrument ID.
            symbol: Instrument symbol.
            price: Entry price.
            date: Entry date.
            target_value: Target position value.
            config: Backtest configuration.

        Returns:
            Tuple of (Position or None, cost).
        """
        slippage = price * config.slippage_pct
        execution_price = price + slippage

        quantity = int(target_value / execution_price)
        if quantity <= 0:
            return None, 0.0

        position_value = quantity * execution_price
        commission = position_value * config.commission_pct
        total_cost = position_value + commission

        position = Position(
            instrument_id=instrument_id,
            symbol=symbol,
            quantity=quantity,
            entry_price=execution_price,
            entry_date=date,
            entry_value=total_cost,
        )

        return position, total_cost

    def _close_position(
        self,
        position: Position,
        price: float,
        date: str,
        reason: str,
        config: BacktestConfig,
    ) -> tuple[Trade, float]:
        """Close an existing position.

        Args:
            position: Position to close.
            price: Exit price.
            date: Exit date.
            reason: Exit reason.
            config: Backtest configuration.

        Returns:
            Tuple of (Trade, net proceeds).
        """
        slippage = price * config.slippage_pct
        execution_price = price - slippage

        gross_proceeds = position.quantity * execution_price
        commission = gross_proceeds * config.commission_pct
        net_proceeds = gross_proceeds - commission

        gross_pnl = gross_proceeds - (position.quantity * position.entry_price)
        entry_commission = position.entry_value - position.quantity * position.entry_price
        total_commission = entry_commission + commission
        net_pnl = gross_pnl - total_commission

        pnl_percent = net_pnl / position.entry_value if position.entry_value > 0 else 0

        trade = Trade(
            instrument_id=position.instrument_id,
            symbol=position.symbol,
            entry_date=position.entry_date,
            entry_price=position.entry_price,
            exit_date=date,
            exit_price=execution_price,
            quantity=position.quantity,
            side="buy",
            pnl=net_pnl,
            pnl_percent=pnl_percent,
            exit_reason=reason,
            commission=total_commission,
        )

        return trade, net_proceeds

    def _calculate_metrics(
        self,
        trades: list[Trade],
        equity_curve: list[tuple[str, float]],
        initial_capital: float,
        final_capital: float,
        total_days: int,
        days_with_positions: int,
    ) -> BacktestMetrics:
        """Calculate performance metrics.

        Args:
            trades: List of completed trades.
            equity_curve: Daily equity values.
            initial_capital: Starting capital.
            final_capital: Ending capital.
            total_days: Total trading days.
            days_with_positions: Days with open positions.

        Returns:
            BacktestMetrics with calculated values.
        """
        total_return = (final_capital - initial_capital) / initial_capital

        years = total_days / 252 if total_days > 0 else 1
        annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0

        winning_trades = [t for t in trades if t.pnl > 0]
        losing_trades = [t for t in trades if t.pnl <= 0]

        win_rate = len(winning_trades) / len(trades) if trades else 0

        gross_profit = sum(t.pnl for t in winning_trades) if winning_trades else 0
        gross_loss = abs(sum(t.pnl for t in losing_trades)) if losing_trades else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else None

        avg_win = gross_profit / len(winning_trades) if winning_trades else None
        avg_loss = gross_loss / len(losing_trades) if losing_trades else None

        largest_win = max((t.pnl for t in trades), default=None) if trades else None
        largest_loss = min((t.pnl for t in trades), default=None) if trades else None

        max_drawdown = 0.0
        max_drawdown_duration = 0
        peak = initial_capital
        drawdown_start = 0

        for i, (date, value) in enumerate(equity_curve):
            if value > peak:
                peak = value
                drawdown_start = i
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_duration = i - drawdown_start

        exposure_time = days_with_positions / total_days if total_days > 0 else 0

        holding_periods = []
        for t in trades:
            try:
                entry = datetime.strptime(t.entry_date, "%Y-%m-%d")
                exit_dt = datetime.strptime(t.exit_date, "%Y-%m-%d")
                holding_periods.append((exit_dt - entry).days)
            except (ValueError, TypeError):
                pass

        avg_holding_period = (
            sum(holding_periods) / len(holding_periods) if holding_periods else None
        )

        daily_returns = []
        for i in range(1, len(equity_curve)):
            prev_value = equity_curve[i - 1][1]
            curr_value = equity_curve[i][1]
            if prev_value > 0:
                daily_returns.append((curr_value - prev_value) / prev_value)

        sharpe_ratio = None
        sortino_ratio = None
        if daily_returns:
            import statistics

            mean_return = statistics.mean(daily_returns)
            std_return = statistics.stdev(daily_returns) if len(daily_returns) > 1 else 0

            if std_return > 0:
                sharpe_ratio = (mean_return * 252) / (std_return * (252**0.5))

            downside_returns = [r for r in daily_returns if r < 0]
            if downside_returns:
                if len(downside_returns) > 1:
                    downside_std = statistics.stdev(downside_returns)
                else:
                    downside_std = 0
                if downside_std > 0:
                    sortino_ratio = (mean_return * 252) / (downside_std * (252**0.5))

        return BacktestMetrics(
            total_return=total_return,
            annualized_return=annualized_return,
            sharpe_ratio=sharpe_ratio,
            sortino_ratio=sortino_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_duration=max_drawdown_duration,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            avg_win=avg_win,
            avg_loss=avg_loss,
            largest_win=largest_win,
            largest_loss=largest_loss,
            avg_holding_period_days=avg_holding_period,
            exposure_time=exposure_time,
        )

    def _persist_trades(self, run_id: int, trades: list[Trade]) -> None:
        """Persist trades to database.

        Args:
            run_id: Backtest run ID.
            trades: List of trades.
        """
        if not trades:
            return

        trade_records = [
            {
                "backtest_run_id": run_id,
                "instrument_id": t.instrument_id,
                "entry_date": t.entry_date,
                "entry_price": t.entry_price,
                "exit_date": t.exit_date,
                "exit_price": t.exit_price,
                "quantity": t.quantity,
                "side": t.side,
                "pnl": t.pnl,
                "pnl_percent": t.pnl_percent,
                "exit_reason": t.exit_reason,
            }
            for t in trades
        ]

        self.db.bulk_insert_backtest_trades(trade_records)

    def _persist_metrics(self, run_id: int, metrics: BacktestMetrics) -> None:
        """Persist metrics to database.

        Args:
            run_id: Backtest run ID.
            metrics: Calculated metrics.
        """
        self.db.insert_backtest_metrics(
            backtest_run_id=run_id,
            metrics={
                "total_return": metrics.total_return,
                "annualized_return": metrics.annualized_return,
                "sharpe_ratio": metrics.sharpe_ratio,
                "sortino_ratio": metrics.sortino_ratio,
                "max_drawdown": metrics.max_drawdown,
                "max_drawdown_duration": metrics.max_drawdown_duration,
                "win_rate": metrics.win_rate,
                "profit_factor": metrics.profit_factor,
                "total_trades": metrics.total_trades,
                "winning_trades": metrics.winning_trades,
                "losing_trades": metrics.losing_trades,
                "avg_win": metrics.avg_win,
                "avg_loss": metrics.avg_loss,
                "largest_win": metrics.largest_win,
                "largest_loss": metrics.largest_loss,
                "avg_holding_period_days": metrics.avg_holding_period_days,
                "exposure_time": metrics.exposure_time,
            },
        )
