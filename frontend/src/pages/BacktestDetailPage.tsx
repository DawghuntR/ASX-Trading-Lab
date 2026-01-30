import { useMemo } from "react";
import { useParams, Link } from "react-router-dom";
import Card from "../components/Card";
import { useBacktestDetail } from "../hooks/useData";
import { isSupabaseConfigured } from "../lib/supabase";
import type { BacktestTradeWithInstrument } from "../api/data";
import styles from "./BacktestDetailPage.module.css";

function formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString("en-AU", {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}

function formatPercent(value: number | null, decimals: number = 2): string {
    if (value === null) return "--";
    const sign = value >= 0 ? "+" : "";
    return `${sign}${(value * 100).toFixed(decimals)}%`;
}

function formatCurrency(value: number | null): string {
    if (value === null) return "--";
    return new Intl.NumberFormat("en-AU", {
        style: "currency",
        currency: "AUD",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);
}

function formatNumber(value: number | null, decimals: number = 2): string {
    if (value === null) return "--";
    return value.toFixed(decimals);
}

function MetricCard({
    label,
    value,
    valueClass,
}: {
    label: string;
    value: string;
    valueClass?: string;
}) {
    return (
        <div className={styles.metricCard}>
            <span className={`${styles.metricValue} ${valueClass || ""}`}>
                {value}
            </span>
            <span className={styles.metricLabel}>{label}</span>
        </div>
    );
}

function TradeRow({ trade }: { trade: BacktestTradeWithInstrument }) {
    const pnlClass =
        trade.pnl !== null
            ? trade.pnl >= 0
                ? styles.positive
                : styles.negative
            : "";

    return (
        <tr className={styles.tradeRow}>
            <td className={styles.symbolCell}>
                <Link
                    to={`/symbol/${trade.instruments?.symbol}`}
                    className={styles.symbolLink}>
                    {trade.instruments?.symbol || "--"}
                </Link>
            </td>
            <td className={styles.sideCell}>
                <span
                    className={`${styles.sideBadge} ${
                        trade.side === "buy" ? styles.sideBuy : styles.sideSell
                    }`}>
                    {trade.side}
                </span>
            </td>
            <td className={styles.dateCell}>{formatDate(trade.entry_date)}</td>
            <td className={styles.priceCell}>
                {formatCurrency(trade.entry_price)}
            </td>
            <td className={styles.dateCell}>
                {trade.exit_date ? formatDate(trade.exit_date) : "--"}
            </td>
            <td className={styles.priceCell}>
                {trade.exit_price ? formatCurrency(trade.exit_price) : "--"}
            </td>
            <td className={styles.quantityCell}>{trade.quantity}</td>
            <td className={`${styles.pnlCell} ${pnlClass}`}>
                {formatCurrency(trade.pnl)}
            </td>
            <td className={`${styles.pnlPercentCell} ${pnlClass}`}>
                {formatPercent(trade.pnl_percent)}
            </td>
            <td className={styles.reasonCell}>{trade.exit_reason || "--"}</td>
        </tr>
    );
}

function EquityCurve({ trades }: { trades: BacktestTradeWithInstrument[] }) {
    const equityData = useMemo(() => {
        if (!trades || trades.length === 0) return [];

        const sortedTrades = [...trades]
            .filter((t) => t.exit_date && t.pnl !== null)
            .sort(
                (a, b) =>
                    new Date(a.exit_date!).getTime() -
                    new Date(b.exit_date!).getTime()
            );

        let cumulative = 0;
        return sortedTrades.map((t) => {
            cumulative += t.pnl || 0;
            return {
                date: t.exit_date!,
                equity: cumulative,
            };
        });
    }, [trades]);

    if (equityData.length === 0) {
        return (
            <div className={styles.noChart}>
                No completed trades to display equity curve
            </div>
        );
    }

    const maxEquity = Math.max(...equityData.map((d) => d.equity));
    const minEquity = Math.min(...equityData.map((d) => d.equity));
    const range = maxEquity - minEquity || 1;
    const height = 200;
    const width = 100;

    const points = equityData
        .map((d, i) => {
            const x = (i / (equityData.length - 1 || 1)) * width;
            const y = height - ((d.equity - minEquity) / range) * height;
            return `${x},${y}`;
        })
        .join(" ");

    const finalEquity = equityData[equityData.length - 1]?.equity || 0;
    const equityClass = finalEquity >= 0 ? styles.positive : styles.negative;

    return (
        <div className={styles.chartContainer}>
            <div className={styles.chartHeader}>
                <span className={styles.chartTitle}>Cumulative P&L</span>
                <span className={`${styles.chartValue} ${equityClass}`}>
                    {formatCurrency(finalEquity)}
                </span>
            </div>
            <svg
                viewBox={`0 0 ${width} ${height}`}
                className={styles.chart}
                preserveAspectRatio="none">
                <line
                    x1="0"
                    y1={height - ((0 - minEquity) / range) * height}
                    x2={width}
                    y2={height - ((0 - minEquity) / range) * height}
                    className={styles.zeroLine}
                />
                <polyline
                    points={points}
                    fill="none"
                    className={`${styles.equityLine} ${equityClass}`}
                />
            </svg>
            <div className={styles.chartLabels}>
                <span>{formatDate(equityData[0].date)}</span>
                <span>{formatDate(equityData[equityData.length - 1].date)}</span>
            </div>
        </div>
    );
}

function BacktestDetailPage() {
    const { id } = useParams<{ id: string }>();
    const runId = id ? parseInt(id, 10) : null;

    const { data, loading, error } = useBacktestDetail(runId);

    if (!isSupabaseConfigured) {
        return (
            <div className={styles.page}>
                <div className={styles.emptyState}>
                    <div className={styles.icon}>🔌</div>
                    <h3>Supabase Not Configured</h3>
                    <p>Configure your Supabase connection to view backtest details.</p>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className={styles.page}>
                <div className={styles.loading}>Loading backtest details...</div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className={styles.page}>
                <div className={styles.error}>
                    <h3>Error Loading Backtest</h3>
                    <p>{error?.message || "Backtest not found"}</p>
                    <Link to="/backtests" className={styles.backLink}>
                        ← Back to Backtests
                    </Link>
                </div>
            </div>
        );
    }

    const { run, metrics, trades } = data;

    const totalReturn =
        run.final_capital && run.initial_capital
            ? (run.final_capital - run.initial_capital) / run.initial_capital
            : null;

    const returnClass =
        totalReturn !== null
            ? totalReturn >= 0
                ? styles.positive
                : styles.negative
            : "";

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <Link to="/backtests" className={styles.backLink}>
                    ← Back to Backtests
                </Link>
                <div className={styles.titleRow}>
                    <h1 className={styles.title}>
                        Backtest #{run.id}
                        {run.name && (
                            <span className={styles.runName}> - {run.name}</span>
                        )}
                    </h1>
                    <span
                        className={`${styles.statusBadge} ${
                            run.status === "completed"
                                ? styles.statusCompleted
                                : run.status === "running"
                                ? styles.statusRunning
                                : run.status === "failed"
                                ? styles.statusFailed
                                : styles.statusPending
                        }`}>
                        {run.status}
                    </span>
                </div>
                <p className={styles.subtitle}>
                    <strong>{run.strategies?.name || "Unknown Strategy"}</strong>
                    {" • "}
                    {formatDate(run.start_date)} to {formatDate(run.end_date)}
                </p>
            </header>

            <section className={styles.summaryGrid}>
                <MetricCard
                    label="Initial Capital"
                    value={formatCurrency(run.initial_capital)}
                />
                <MetricCard
                    label="Final Capital"
                    value={formatCurrency(run.final_capital)}
                />
                <MetricCard
                    label="Total Return"
                    value={formatPercent(totalReturn)}
                    valueClass={returnClass}
                />
                <MetricCard
                    label="Total Trades"
                    value={metrics?.total_trades?.toString() || "--"}
                />
            </section>

            {metrics && (
                <section className={styles.metricsSection}>
                    <Card title="Performance Metrics">
                        <div className={styles.metricsGrid}>
                            <MetricCard
                                label="Annualized Return"
                                value={formatPercent(metrics.annualized_return)}
                                valueClass={
                                    metrics.annualized_return !== null
                                        ? metrics.annualized_return >= 0
                                            ? styles.positive
                                            : styles.negative
                                        : ""
                                }
                            />
                            <MetricCard
                                label="Sharpe Ratio"
                                value={formatNumber(metrics.sharpe_ratio)}
                            />
                            <MetricCard
                                label="Sortino Ratio"
                                value={formatNumber(metrics.sortino_ratio)}
                            />
                            <MetricCard
                                label="Max Drawdown"
                                value={formatPercent(metrics.max_drawdown)}
                                valueClass={styles.negative}
                            />
                            <MetricCard
                                label="Win Rate"
                                value={formatPercent(metrics.win_rate)}
                            />
                            <MetricCard
                                label="Profit Factor"
                                value={formatNumber(metrics.profit_factor)}
                            />
                            <MetricCard
                                label="Winning Trades"
                                value={metrics.winning_trades?.toString() || "--"}
                            />
                            <MetricCard
                                label="Losing Trades"
                                value={metrics.losing_trades?.toString() || "--"}
                            />
                            <MetricCard
                                label="Avg Win"
                                value={formatCurrency(metrics.avg_win)}
                                valueClass={styles.positive}
                            />
                            <MetricCard
                                label="Avg Loss"
                                value={formatCurrency(metrics.avg_loss)}
                                valueClass={styles.negative}
                            />
                            <MetricCard
                                label="Largest Win"
                                value={formatCurrency(metrics.largest_win)}
                                valueClass={styles.positive}
                            />
                            <MetricCard
                                label="Largest Loss"
                                value={formatCurrency(metrics.largest_loss)}
                                valueClass={styles.negative}
                            />
                            <MetricCard
                                label="Avg Holding Period"
                                value={
                                    metrics.avg_holding_period_days !== null
                                        ? `${formatNumber(
                                              metrics.avg_holding_period_days,
                                              1
                                          )} days`
                                        : "--"
                                }
                            />
                            <MetricCard
                                label="Exposure Time"
                                value={formatPercent(metrics.exposure_time)}
                            />
                        </div>
                    </Card>
                </section>
            )}

            <section className={styles.chartSection}>
                <Card title="Equity Curve">
                    <EquityCurve trades={trades} />
                </Card>
            </section>

            <section className={styles.tradesSection}>
                <Card title={`Trade Log (${trades.length})`}>
                    {trades.length === 0 ? (
                        <div className={styles.noTrades}>
                            No trades recorded for this backtest
                        </div>
                    ) : (
                        <div className={styles.tableWrapper}>
                            <table className={styles.table}>
                                <thead>
                                    <tr>
                                        <th>Symbol</th>
                                        <th>Side</th>
                                        <th>Entry Date</th>
                                        <th>Entry Price</th>
                                        <th>Exit Date</th>
                                        <th>Exit Price</th>
                                        <th>Qty</th>
                                        <th>P&L</th>
                                        <th>P&L %</th>
                                        <th>Exit Reason</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {trades.map((trade) => (
                                        <TradeRow key={trade.id} trade={trade} />
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </Card>
            </section>
        </div>
    );
}

export default BacktestDetailPage;
