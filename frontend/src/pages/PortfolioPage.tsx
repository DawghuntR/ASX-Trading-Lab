import { useState, useMemo } from "react";
import Card from "../components/Card";
import {
    usePaperAccounts,
    usePortfolioSummary,
    usePaperPositions,
    usePaperOrders,
    usePortfolioSnapshots,
    useRiskMetrics,
} from "../hooks/useData";
import styles from "./PortfolioPage.module.css";

function formatCurrency(value: number | null | undefined): string {
    if (value === null || value === undefined) return "--";
    return new Intl.NumberFormat("en-AU", {
        style: "currency",
        currency: "AUD",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);
}

function formatPercent(value: number | null | undefined): string {
    if (value === null || value === undefined) return "--";
    const sign = value >= 0 ? "+" : "";
    return `${sign}${(value * 100).toFixed(2)}%`;
}

function formatNumber(value: number | null | undefined): string {
    if (value === null || value === undefined) return "--";
    return new Intl.NumberFormat("en-AU").format(value);
}

function PortfolioPage() {
    const { data: accounts, loading: accountsLoading } = usePaperAccounts();
    const [selectedAccountId, setSelectedAccountId] = useState<number | null>(
        null
    );

    const activeAccountId = useMemo(() => {
        if (selectedAccountId !== null) return selectedAccountId;
        if (accounts && accounts.length > 0) return accounts[0].id;
        return null;
    }, [selectedAccountId, accounts]);

    const { data: summary, loading: summaryLoading } =
        usePortfolioSummary(activeAccountId);
    const { data: positions, loading: positionsLoading } =
        usePaperPositions(activeAccountId);
    const { data: orders, loading: ordersLoading } = usePaperOrders(
        activeAccountId,
        undefined,
        20
    );
    const { data: snapshots } = usePortfolioSnapshots(activeAccountId, 90);

    const riskMetrics = useRiskMetrics(summary, snapshots);

    const isLoading =
        accountsLoading || summaryLoading || positionsLoading || ordersLoading;

    const latestSnapshot = snapshots && snapshots.length > 0 ? snapshots[0] : null;
    const dailyPnl = latestSnapshot?.daily_pnl ?? null;
    const dailyReturn = latestSnapshot?.daily_return ?? null;

    const equityCurveData = useMemo(() => {
        if (!snapshots || snapshots.length === 0) return [];
        return [...snapshots].reverse().slice(-30);
    }, [snapshots]);

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <div className={styles.headerTop}>
                    <div>
                        <h1 className={styles.title}>Portfolio</h1>
                        <p className={styles.subtitle}>
                            Paper trading portfolio and risk metrics
                        </p>
                    </div>
                    {accounts && accounts.length > 0 && (
                        <div className={styles.accountSelector}>
                            <label htmlFor="account-select">Account:</label>
                            <select
                                id="account-select"
                                value={activeAccountId ?? ""}
                                onChange={(e) =>
                                    setSelectedAccountId(
                                        e.target.value
                                            ? Number(e.target.value)
                                            : null
                                    )
                                }
                                className={styles.select}
                            >
                                {accounts.map((acc) => (
                                    <option key={acc.id} value={acc.id}>
                                        {acc.name}
                                    </option>
                                ))}
                            </select>
                        </div>
                    )}
                </div>
            </header>

            {isLoading ? (
                <div className={styles.loading}>Loading portfolio data...</div>
            ) : !accounts || accounts.length === 0 ? (
                <div className={styles.emptyState}>
                    <h3>No Paper Trading Accounts</h3>
                    <p>
                        Create a paper trading account using the CLI to get
                        started.
                    </p>
                    <code className={styles.codeHint}>
                        asx-jobs paper account create "My Account" --balance
                        100000
                    </code>
                </div>
            ) : (
                <>
                    <div className={styles.grid}>
                        <Card title="Portfolio Summary">
                            <div className={styles.metricsGrid}>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Total Value
                                    </span>
                                    <span className={styles.metricValue}>
                                        {formatCurrency(summary?.total_value)}
                                    </span>
                                </div>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Daily P&L
                                    </span>
                                    <span
                                        className={`${styles.metricValue} ${
                                            dailyPnl !== null
                                                ? dailyPnl >= 0
                                                    ? styles.positive
                                                    : styles.negative
                                                : ""
                                        }`}
                                    >
                                        {formatCurrency(dailyPnl)}
                                    </span>
                                    {dailyReturn !== null && (
                                        <span
                                            className={`${styles.metricSubvalue} ${
                                                dailyReturn >= 0
                                                    ? styles.positive
                                                    : styles.negative
                                            }`}
                                        >
                                            {formatPercent(dailyReturn)}
                                        </span>
                                    )}
                                </div>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Total Return
                                    </span>
                                    <span
                                        className={`${styles.metricValue} ${
                                            summary?.total_return_percent !==
                                                null &&
                                            summary?.total_return_percent !==
                                                undefined
                                                ? summary.total_return_percent >=
                                                  0
                                                    ? styles.positive
                                                    : styles.negative
                                                : ""
                                        }`}
                                    >
                                        {formatPercent(
                                            summary?.total_return_percent
                                                ? summary.total_return_percent /
                                                      100
                                                : null
                                        )}
                                    </span>
                                </div>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Open Positions
                                    </span>
                                    <span className={styles.metricValue}>
                                        {summary?.open_positions ?? "--"}
                                    </span>
                                </div>
                            </div>
                        </Card>

                        <Card
                            title="Risk Status"
                            className={
                                !riskMetrics.is_compliant
                                    ? styles.riskWarning
                                    : ""
                            }
                        >
                            <div className={styles.riskStatus}>
                                <div
                                    className={`${styles.complianceBadge} ${
                                        riskMetrics.is_compliant
                                            ? styles.compliant
                                            : styles.violation
                                    }`}
                                >
                                    {riskMetrics.is_compliant
                                        ? "COMPLIANT"
                                        : "VIOLATIONS"}
                                </div>
                            </div>
                            <div className={styles.metricsGrid}>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Exposure
                                    </span>
                                    <span
                                        className={`${styles.metricValue} ${
                                            riskMetrics.total_exposure > 0.95
                                                ? styles.negative
                                                : ""
                                        }`}
                                    >
                                        {(
                                            riskMetrics.total_exposure * 100
                                        ).toFixed(1)}
                                        %
                                    </span>
                                </div>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Drawdown
                                    </span>
                                    <span
                                        className={`${styles.metricValue} ${
                                            riskMetrics.current_drawdown_pct >
                                            0.2
                                                ? styles.negative
                                                : riskMetrics.current_drawdown_pct >
                                                    0.1
                                                  ? styles.warning
                                                  : ""
                                        }`}
                                    >
                                        {(
                                            riskMetrics.current_drawdown_pct *
                                            100
                                        ).toFixed(1)}
                                        %
                                    </span>
                                </div>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Cash Reserve
                                    </span>
                                    <span
                                        className={`${styles.metricValue} ${
                                            riskMetrics.cash_reserve_pct < 0.05
                                                ? styles.negative
                                                : ""
                                        }`}
                                    >
                                        {(
                                            riskMetrics.cash_reserve_pct * 100
                                        ).toFixed(1)}
                                        %
                                    </span>
                                </div>
                                <div className={styles.metric}>
                                    <span className={styles.metricLabel}>
                                        Peak Value
                                    </span>
                                    <span className={styles.metricValue}>
                                        {formatCurrency(riskMetrics.peak_value)}
                                    </span>
                                </div>
                            </div>
                            {riskMetrics.violations.length > 0 && (
                                <div className={styles.violations}>
                                    {riskMetrics.violations.map((v, i) => (
                                        <div
                                            key={i}
                                            className={styles.violationItem}
                                        >
                                            {v}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </Card>
                    </div>

                    {equityCurveData.length > 0 && (
                        <section className={styles.chartSection}>
                            <Card title="Equity Curve (Last 30 Days)">
                                <div className={styles.equityChart}>
                                    <div className={styles.chartBars}>
                                        {equityCurveData.map((snap, i) => {
                                            const minVal = Math.min(
                                                ...equityCurveData.map(
                                                    (s) => s.total_value
                                                )
                                            );
                                            const maxVal = Math.max(
                                                ...equityCurveData.map(
                                                    (s) => s.total_value
                                                )
                                            );
                                            const range = maxVal - minVal || 1;
                                            const height =
                                                ((snap.total_value - minVal) /
                                                    range) *
                                                    80 +
                                                20;
                                            const isPositive =
                                                (snap.daily_pnl ?? 0) >= 0;
                                            return (
                                                <div
                                                    key={i}
                                                    className={`${styles.chartBar} ${isPositive ? styles.positive : styles.negative}`}
                                                    style={{
                                                        height: `${height}%`,
                                                    }}
                                                    title={`${snap.snapshot_date}: ${formatCurrency(snap.total_value)}`}
                                                />
                                            );
                                        })}
                                    </div>
                                    <div className={styles.chartLabels}>
                                        <span>
                                            {equityCurveData[0]?.snapshot_date}
                                        </span>
                                        <span>
                                            {
                                                equityCurveData[
                                                    equityCurveData.length - 1
                                                ]?.snapshot_date
                                            }
                                        </span>
                                    </div>
                                </div>
                            </Card>
                        </section>
                    )}

                    <section className={styles.positions}>
                        <Card title="Current Positions">
                            {positions && positions.length > 0 ? (
                                <div className={styles.tableWrapper}>
                                    <table className={styles.table}>
                                        <thead>
                                            <tr>
                                                <th>Symbol</th>
                                                <th>Name</th>
                                                <th className={styles.right}>
                                                    Qty
                                                </th>
                                                <th className={styles.right}>
                                                    Avg Entry
                                                </th>
                                                <th className={styles.right}>
                                                    Current
                                                </th>
                                                <th className={styles.right}>
                                                    Unrealized P&L
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {positions.map((pos) => {
                                                const pnl =
                                                    pos.unrealized_pnl ?? 0;
                                                const pnlPct =
                                                    pos.avg_entry_price > 0
                                                        ? ((pos.current_price ??
                                                              pos.avg_entry_price) -
                                                              pos.avg_entry_price) /
                                                          pos.avg_entry_price
                                                        : 0;
                                                return (
                                                    <tr key={pos.id}>
                                                        <td
                                                            className={
                                                                styles.symbol
                                                            }
                                                        >
                                                            {pos.instruments
                                                                ?.symbol ??
                                                                "N/A"}
                                                        </td>
                                                        <td
                                                            className={
                                                                styles.name
                                                            }
                                                        >
                                                            {pos.instruments
                                                                ?.name ?? "--"}
                                                        </td>
                                                        <td
                                                            className={
                                                                styles.right
                                                            }
                                                        >
                                                            {formatNumber(
                                                                pos.quantity
                                                            )}
                                                        </td>
                                                        <td
                                                            className={
                                                                styles.right
                                                            }
                                                        >
                                                            {formatCurrency(
                                                                pos.avg_entry_price
                                                            )}
                                                        </td>
                                                        <td
                                                            className={
                                                                styles.right
                                                            }
                                                        >
                                                            {formatCurrency(
                                                                pos.current_price
                                                            )}
                                                        </td>
                                                        <td
                                                            className={`${styles.right} ${pnl >= 0 ? styles.positive : styles.negative}`}
                                                        >
                                                            {formatCurrency(
                                                                pnl
                                                            )}{" "}
                                                            <span
                                                                className={
                                                                    styles.pnlPct
                                                                }
                                                            >
                                                                (
                                                                {formatPercent(
                                                                    pnlPct
                                                                )}
                                                                )
                                                            </span>
                                                        </td>
                                                    </tr>
                                                );
                                            })}
                                        </tbody>
                                    </table>
                                </div>
                            ) : (
                                <div className={styles.emptyState}>
                                    <p>No open positions.</p>
                                </div>
                            )}
                        </Card>
                    </section>

                    <section className={styles.history}>
                        <Card title="Recent Orders">
                            {orders && orders.length > 0 ? (
                                <div className={styles.tableWrapper}>
                                    <table className={styles.table}>
                                        <thead>
                                            <tr>
                                                <th>Date</th>
                                                <th>Symbol</th>
                                                <th>Side</th>
                                                <th className={styles.right}>
                                                    Qty
                                                </th>
                                                <th className={styles.right}>
                                                    Price
                                                </th>
                                                <th>Status</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {orders.map((order) => (
                                                <tr key={order.id}>
                                                    <td>
                                                        {order.submitted_at
                                                            ? new Date(
                                                                  order.submitted_at
                                                              ).toLocaleDateString()
                                                            : "--"}
                                                    </td>
                                                    <td
                                                        className={
                                                            styles.symbol
                                                        }
                                                    >
                                                        {order.instruments
                                                            ?.symbol ?? "N/A"}
                                                    </td>
                                                    <td>
                                                        <span
                                                            className={`${styles.sideBadge} ${order.order_side === "buy" ? styles.buy : styles.sell}`}
                                                        >
                                                            {order.order_side.toUpperCase()}
                                                        </span>
                                                    </td>
                                                    <td
                                                        className={styles.right}
                                                    >
                                                        {formatNumber(
                                                            order.quantity
                                                        )}
                                                    </td>
                                                    <td
                                                        className={styles.right}
                                                    >
                                                        {formatCurrency(
                                                            order.filled_avg_price ??
                                                                order.limit_price
                                                        )}
                                                    </td>
                                                    <td>
                                                        <span
                                                            className={`${styles.statusBadge} ${styles[order.status]}`}
                                                        >
                                                            {order.status}
                                                        </span>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            ) : (
                                <div className={styles.emptyState}>
                                    <p>No orders yet.</p>
                                </div>
                            )}
                        </Card>
                    </section>
                </>
            )}
        </div>
    );
}

export default PortfolioPage;
