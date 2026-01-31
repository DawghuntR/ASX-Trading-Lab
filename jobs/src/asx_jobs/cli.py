"""Command-line interface for ASX Jobs Runner."""

import argparse
import sys
from datetime import datetime
from typing import Any

from asx_jobs.config import load_config
from asx_jobs.database import Database
from asx_jobs.logging import get_logger, setup_logging
from asx_jobs.orchestrator import JobOrchestrator
from asx_jobs.paper import EODExecutor, PaperTradingEngine, PortfolioAnalyzer, RiskManager


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="ASX Trading Lab Jobs Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  asx-jobs daily                  Run daily ingestion + signal generation
  asx-jobs backfill --period 2y   Backfill 2 years of historical data
  asx-jobs symbols                Ingest symbols only (with metadata)
  asx-jobs signals                Generate signals only
  asx-jobs announcements          Ingest ASX announcements only
  asx-jobs reactions              Compute 1D reaction metrics for announcements

Paper Trading:
  asx-jobs paper account create "My Account" --balance 100000
  asx-jobs paper account list
  asx-jobs paper order buy BHP 100 --account 1
  asx-jobs paper order sell CBA 50 --account 1 --limit 95.00
  asx-jobs paper execute --date 2024-01-15
  asx-jobs paper positions --account 1
  asx-jobs paper snapshot --account 1
  asx-jobs paper metrics --account 1
  asx-jobs paper risk --account 1
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Daily command
    subparsers.add_parser("daily", help="Run daily ingestion + signal generation")

    # Backfill command
    backfill_parser = subparsers.add_parser("backfill", help="Backfill historical data")
    backfill_parser.add_argument(
        "--period",
        default="2y",
        help="Backfill period (e.g., 1y, 2y, 5y, max). Default: 2y",
    )

    # Symbols command
    symbols_parser = subparsers.add_parser("symbols", help="Ingest symbols only")
    symbols_parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Skip fetching metadata for symbols",
    )

    # Signals command
    subparsers.add_parser("signals", help="Generate signals only")

    # Announcements command
    subparsers.add_parser("announcements", help="Ingest ASX announcements")

    # Reactions command
    reactions_parser = subparsers.add_parser(
        "reactions", help="Compute announcement reaction metrics"
    )
    reactions_parser.add_argument(
        "--lookback",
        type=int,
        default=90,
        help="Number of days to look back for announcements (default: 90)",
    )

    # Paper trading command
    paper_parser = subparsers.add_parser("paper", help="Paper trading operations")
    paper_subparsers = paper_parser.add_subparsers(dest="paper_command")

    # Paper account commands
    account_parser = paper_subparsers.add_parser("account", help="Account management")
    account_subparsers = account_parser.add_subparsers(dest="account_command")

    account_create = account_subparsers.add_parser("create", help="Create account")
    account_create.add_argument("name", help="Account name")
    account_create.add_argument("--balance", type=float, default=100000.0, help="Initial balance")

    account_subparsers.add_parser("list", help="List accounts")

    account_show = account_subparsers.add_parser("show", help="Show account details")
    account_show.add_argument("account_id", type=int, help="Account ID")

    # Paper order commands
    order_parser = paper_subparsers.add_parser("order", help="Order management")
    order_subparsers = order_parser.add_subparsers(dest="order_command")

    order_buy = order_subparsers.add_parser("buy", help="Submit buy order")
    order_buy.add_argument("symbol", help="Stock symbol")
    order_buy.add_argument("quantity", type=int, help="Number of shares")
    order_buy.add_argument("--account", type=int, required=True, help="Account ID")
    order_buy.add_argument("--limit", type=float, help="Limit price")

    order_sell = order_subparsers.add_parser("sell", help="Submit sell order")
    order_sell.add_argument("symbol", help="Stock symbol")
    order_sell.add_argument("quantity", type=int, help="Number of shares")
    order_sell.add_argument("--account", type=int, required=True, help="Account ID")
    order_sell.add_argument("--limit", type=float, help="Limit price")

    order_list = order_subparsers.add_parser("list", help="List orders")
    order_list.add_argument("--account", type=int, required=True, help="Account ID")
    order_list.add_argument("--status", help="Filter by status")

    order_cancel = order_subparsers.add_parser("cancel", help="Cancel order")
    order_cancel.add_argument("order_id", type=int, help="Order ID")

    # Paper execute command
    execute_parser = paper_subparsers.add_parser("execute", help="Execute pending orders at EOD")
    execute_parser.add_argument("--date", help="Execution date (YYYY-MM-DD)")
    execute_parser.add_argument("--account", type=int, help="Account ID filter")

    # Paper positions command
    positions_parser = paper_subparsers.add_parser("positions", help="Show positions")
    positions_parser.add_argument("--account", type=int, required=True, help="Account ID")

    # Paper snapshot command
    snapshot_parser = paper_subparsers.add_parser("snapshot", help="Create portfolio snapshot")
    snapshot_parser.add_argument("--account", type=int, required=True, help="Account ID")
    snapshot_parser.add_argument("--date", help="Snapshot date (YYYY-MM-DD)")

    # Paper metrics command
    metrics_parser = paper_subparsers.add_parser(
        "metrics", help="Show portfolio performance metrics"
    )
    metrics_parser.add_argument("--account", type=int, required=True, help="Account ID")
    metrics_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Paper risk command
    risk_parser = paper_subparsers.add_parser("risk", help="Show risk metrics and violations")
    risk_parser.add_argument("--account", type=int, required=True, help="Account ID")
    risk_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Global options
    parser.add_argument(
        "--env-file",
        help="Path to .env file",
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level. Default: INFO",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    setup_logging(args.log_level)
    logger = get_logger("cli")

    try:
        config = load_config(args.env_file)
        config.validate()
    except ValueError as e:
        logger.error("configuration_error", error=str(e))
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1

    # Handle paper trading commands
    if args.command == "paper":
        return handle_paper_command(args, config)

    # Handle job commands
    orchestrator = JobOrchestrator(config)

    try:
        if args.command == "daily":
            result = orchestrator.run_daily()
        elif args.command == "backfill":
            result = orchestrator.run_backfill(period=args.period)
        elif args.command == "symbols":
            result = orchestrator.run_symbols_only(fetch_metadata=not args.no_metadata)
        elif args.command == "signals":
            result = orchestrator.run_signals()
        elif args.command == "announcements":
            result = orchestrator.run_announcements()
        elif args.command == "reactions":
            result = orchestrator.run_reactions(lookback_days=args.lookback)
        else:
            logger.error("unknown_command", command=args.command)
            return 1

        for job_result in result.results:
            status = "SUCCESS" if job_result.success else "FAILED"
            print(
                f"[{status}] {job_result.job_name}: "
                f"{job_result.records_processed} processed, "
                f"{job_result.records_failed} failed "
                f"({job_result.duration_seconds:.1f}s)"
            )
            if job_result.error_message:
                print(f"  Errors: {job_result.error_message}")

        print(f"\nTotal: {result.jobs_succeeded}/{result.jobs_run} jobs succeeded")
        print(f"Duration: {result.duration_seconds:.1f}s")

        return 0 if result.success else 1

    except KeyboardInterrupt:
        logger.warning("interrupted")
        print("\nInterrupted by user", file=sys.stderr)
        return 130

    except Exception as e:
        logger.error("fatal_error", error=str(e), exc_info=True)
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


def handle_paper_command(args: argparse.Namespace, config: Any) -> int:
    """Handle paper trading commands.

    Args:
        args: Parsed command-line arguments.
        config: Application configuration.

    Returns:
        Exit code.
    """
    db = Database(config.supabase)
    engine = PaperTradingEngine(db)
    executor = EODExecutor(db)
    analyzer = PortfolioAnalyzer(db)
    risk_manager = RiskManager(db)

    if args.paper_command == "account":
        return handle_account_command(args, engine)
    elif args.paper_command == "order":
        return handle_order_command(args, engine)
    elif args.paper_command == "execute":
        return handle_execute_command(args, executor)
    elif args.paper_command == "positions":
        return handle_positions_command(args, engine)
    elif args.paper_command == "snapshot":
        return handle_snapshot_command(args, engine)
    elif args.paper_command == "metrics":
        return handle_metrics_command(args, analyzer)
    elif args.paper_command == "risk":
        return handle_risk_command(args, risk_manager)
    else:
        print("Unknown paper command. Use 'asx-jobs paper --help'", file=sys.stderr)
        return 1


def handle_account_command(args: argparse.Namespace, engine: PaperTradingEngine) -> int:
    """Handle account subcommands."""
    if args.account_command == "create":
        try:
            account_id = engine.create_account(args.name, args.balance)
            print(f"Created account '{args.name}' with ID {account_id}")
            print(f"Initial balance: ${args.balance:,.2f}")
            return 0
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.account_command == "list":
        accounts = engine.list_accounts()
        if not accounts:
            print("No paper trading accounts found.")
            return 0

        print(f"{'ID':<6} {'Name':<20} {'Cash Balance':>15} {'Initial':>15}")
        print("-" * 60)
        for acc in accounts:
            print(
                f"{acc['id']:<6} {acc['name']:<20} "
                f"${acc['cash_balance']:>14,.2f} ${acc['initial_balance']:>14,.2f}"
            )
        return 0

    elif args.account_command == "show":
        portfolio = engine.get_portfolio_value(args.account_id)
        if portfolio is None:
            print(f"Account {args.account_id} not found", file=sys.stderr)
            return 1
        acc_data = engine.get_account(args.account_id)
        if not acc_data:
            print(f"Account {args.account_id} not found", file=sys.stderr)
            return 1
        acc = acc_data

        print(f"\nAccount: {acc['name']} (ID: {acc['id']})")
        print("=" * 50)
        print(f"Cash Balance:     ${portfolio['cash_balance']:>15,.2f}")
        print(f"Positions Value:  ${portfolio['positions_value']:>15,.2f}")
        print(f"Total Value:      ${portfolio['total_value']:>15,.2f}")
        print(f"Initial Balance:  ${portfolio['initial_balance']:>15,.2f}")
        print(f"Total Return:     {portfolio['total_return'] * 100:>15.2f}%")

        if portfolio["positions"]:
            header = f"\n{'Symbol':<8} {'Qty':>8} {'Avg Price':>12}"
            header += f" {'Current':>12} {'P&L':>12} {'P&L %':>8}"
            print(header)
            print("-" * 65)
            for pos in portfolio["positions"]:
                print(
                    f"{pos['symbol'] or 'N/A':<8} {pos['quantity']:>8} "
                    f"${pos['avg_entry_price']:>10,.2f} ${pos['current_price']:>10,.2f} "
                    f"${pos['unrealized_pnl']:>10,.2f} {pos['unrealized_pnl_pct'] * 100:>7.2f}%"
                )
        return 0

    print("Unknown account command", file=sys.stderr)
    return 1


def handle_order_command(args: argparse.Namespace, engine: PaperTradingEngine) -> int:
    """Handle order subcommands."""
    if args.order_command in ("buy", "sell"):
        order_type = "limit" if args.limit else "market"
        result = engine.submit_order(
            account_id=args.account,
            symbol=args.symbol.upper(),
            side=args.order_command,
            quantity=args.quantity,
            order_type=order_type,
            limit_price=args.limit,
        )

        if result.success:
            msg = f"Order submitted: {args.order_command.upper()}"
            msg += f" {args.quantity} {args.symbol.upper()}"
            print(msg)
            print(f"Order ID: {result.order_id}")
            if args.limit:
                print(f"Limit Price: ${args.limit:,.2f}")
            print("Status: Pending (will execute at EOD)")
        else:
            print(f"Order failed: {result.message}", file=sys.stderr)
            return 1
        return 0

    elif args.order_command == "list":
        orders = engine.get_orders(args.account, args.status)
        if not orders:
            print("No orders found.")
            return 0

        header = f"{'ID':<6} {'Symbol':<8} {'Side':<6} {'Qty':>8}"
        header += f" {'Type':<8} {'Status':<10} {'Filled':>10}"
        print(header)
        print("-" * 70)
        for order in orders:
            symbol = order["instruments"]["symbol"] if order.get("instruments") else "N/A"
            filled_price = (
                f"${order['filled_avg_price']:.2f}" if order.get("filled_avg_price") else "-"
            )
            print(
                f"{order['id']:<6} {symbol:<8} {order['order_side']:<6} "
                f"{order['quantity']:>8} {order['order_type']:<8} "
                f"{order['status']:<10} {filled_price:>10}"
            )
        return 0

    elif args.order_command == "cancel":
        if engine.cancel_order(args.order_id):
            print(f"Order {args.order_id} cancelled")
            return 0
        else:
            print(f"Could not cancel order {args.order_id}", file=sys.stderr)
            return 1

    print("Unknown order command", file=sys.stderr)
    return 1


def handle_execute_command(args: argparse.Namespace, executor: EODExecutor) -> int:
    """Handle execute command."""
    execution_date = args.date or datetime.now().strftime("%Y-%m-%d")

    print(f"Executing orders for {execution_date}...")
    result = executor.execute_orders(execution_date, args.account)

    print(f"\nExecution Summary for {result.execution_date}")
    print("=" * 50)
    print(f"Orders Processed: {result.orders_processed}")
    print(f"Orders Filled:    {result.orders_filled}")
    print(f"Orders Rejected:  {result.orders_rejected}")
    print(f"Total Buy Value:  ${result.total_buy_value:,.2f}")
    print(f"Total Sell Value: ${result.total_sell_value:,.2f}")

    if result.fills:
        print(f"\n{'Symbol':<8} {'Side':<6} {'Qty':>8} {'Price':>12} {'Value':>14} {'Status':<10}")
        print("-" * 65)
        for fill in result.fills:
            status = "FILLED" if fill.success else "REJECTED"
            print(
                f"{fill.symbol:<8} {fill.side:<6} {fill.quantity:>8} "
                f"${fill.fill_price:>10,.2f} ${fill.total_value:>12,.2f} {status:<10}"
            )
            if not fill.success:
                print(f"  -> {fill.message}")

    return 0


def handle_positions_command(args: argparse.Namespace, engine: PaperTradingEngine) -> int:
    """Handle positions command."""
    positions = engine.get_positions(args.account)

    if not positions:
        print("No open positions.")
        return 0

    print(f"{'Symbol':<8} {'Qty':>10} {'Avg Price':>12} {'Current':>12} {'Unrealized P&L':>15}")
    print("-" * 60)

    for pos in positions:
        symbol = pos["instruments"]["symbol"] if pos.get("instruments") else "N/A"
        current = pos.get("current_price") or pos["avg_entry_price"]
        unrealized = (current - pos["avg_entry_price"]) * pos["quantity"]
        print(
            f"{symbol:<8} {pos['quantity']:>10} ${pos['avg_entry_price']:>10,.2f} "
            f"${current:>10,.2f} ${unrealized:>13,.2f}"
        )

    return 0


def handle_snapshot_command(args: argparse.Namespace, engine: PaperTradingEngine) -> int:
    """Handle snapshot command."""
    snapshot_date = args.date or datetime.now().strftime("%Y-%m-%d")

    try:
        engine.update_position_prices(args.account)
        snapshot_id = engine.create_snapshot(args.account, snapshot_date)
        portfolio = engine.get_portfolio_value(args.account)

        print(f"Portfolio snapshot created for {snapshot_date}")
        print(f"Snapshot ID: {snapshot_id}")
        print(f"Total Value: ${portfolio['total_value']:,.2f}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_metrics_command(args: argparse.Namespace, analyzer: PortfolioAnalyzer) -> int:
    """Handle metrics command."""
    import json
    from dataclasses import asdict

    try:
        metrics = analyzer.compute_metrics(args.account)

        if args.json:
            print(json.dumps(asdict(metrics), indent=2, default=str))
        else:
            report = analyzer.format_report(metrics)
            print(report)

        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_risk_command(args: argparse.Namespace, risk_manager: RiskManager) -> int:
    """Handle risk command."""
    import json
    from dataclasses import asdict

    try:
        metrics = risk_manager.compute_risk_metrics(args.account)

        if args.json:
            print(json.dumps(asdict(metrics), indent=2, default=str))
        else:
            report = risk_manager.format_report(metrics)
            print(report)

        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
