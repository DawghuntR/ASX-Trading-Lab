import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import Card from "../components/Card";
import { useBacktestRuns, useStrategies } from "../hooks/useData";
import { isSupabaseConfigured } from "../lib/supabase";
import type { BacktestRunWithStrategy } from "../api/data";
import styles from "./BacktestsPage.module.css";

function formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString("en-AU", {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}

function formatPercent(value: number | null): string {
    if (value === null) return "--";
    const sign = value >= 0 ? "+" : "";
    return `${sign}${(value * 100).toFixed(2)}%`;
}

function formatCurrency(value: number | null): string {
    if (value === null) return "--";
    return new Intl.NumberFormat("en-AU", {
        style: "currency",
        currency: "AUD",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(value);
}

function BacktestRow({ run }: { run: BacktestRunWithStrategy }) {
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

    const statusClass =
        run.status === "completed"
            ? styles.statusCompleted
            : run.status === "running"
            ? styles.statusRunning
            : run.status === "failed"
            ? styles.statusFailed
            : styles.statusPending;

    return (
        <tr className={styles.row}>
            <td className={styles.idCell}>
                <Link to={`/backtests/${run.id}`} className={styles.idLink}>
                    #{run.id}
                </Link>
            </td>
            <td className={styles.strategyCell}>
                {run.strategies?.name || "Unknown"}
            </td>
            <td className={styles.nameCell}>{run.name || "--"}</td>
            <td className={styles.dateCell}>
                {formatDate(run.start_date)} - {formatDate(run.end_date)}
            </td>
            <td className={styles.capitalCell}>
                {formatCurrency(run.initial_capital)}
            </td>
            <td className={`${styles.returnCell} ${returnClass}`}>
                {formatPercent(totalReturn)}
            </td>
            <td className={styles.statusCell}>
                <span className={`${styles.statusBadge} ${statusClass}`}>
                    {run.status}
                </span>
            </td>
            <td className={styles.actionsCell}>
                <Link
                    to={`/backtests/${run.id}`}
                    className={styles.viewButton}>
                    View
                </Link>
            </td>
        </tr>
    );
}

function BacktestsPage() {
    const [strategyFilter, setStrategyFilter] = useState<string>("all");
    const [statusFilter, setStatusFilter] = useState<string>("all");

    const { data: runs, loading, error } = useBacktestRuns(100);
    const { data: strategies } = useStrategies();

    const filteredRuns = useMemo(() => {
        if (!runs) return [];
        return runs.filter((run) => {
            if (
                strategyFilter !== "all" &&
                run.strategy_id.toString() !== strategyFilter
            ) {
                return false;
            }
            if (statusFilter !== "all" && run.status !== statusFilter) {
                return false;
            }
            return true;
        });
    }, [runs, strategyFilter, statusFilter]);

    const stats = useMemo(() => {
        if (!runs) return { total: 0, completed: 0, avgReturn: null };
        const completed = runs.filter((r) => r.status === "completed");
        const returns = completed
            .map((r) =>
                r.final_capital && r.initial_capital
                    ? (r.final_capital - r.initial_capital) / r.initial_capital
                    : null
            )
            .filter((r): r is number => r !== null);

        const avgReturn =
            returns.length > 0
                ? returns.reduce((a, b) => a + b, 0) / returns.length
                : null;

        return {
            total: runs.length,
            completed: completed.length,
            avgReturn,
        };
    }, [runs]);

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>Backtests</h1>
                <p className={styles.subtitle}>
                    Strategy backtesting results and performance analysis
                </p>
            </header>

            {isSupabaseConfigured && runs && runs.length > 0 && (
                <section className={styles.statsRow}>
                    <div className={styles.statCard}>
                        <span className={styles.statValue}>{stats.total}</span>
                        <span className={styles.statLabel}>Total Runs</span>
                    </div>
                    <div className={styles.statCard}>
                        <span className={styles.statValue}>
                            {stats.completed}
                        </span>
                        <span className={styles.statLabel}>Completed</span>
                    </div>
                    <div className={styles.statCard}>
                        <span
                            className={`${styles.statValue} ${
                                stats.avgReturn !== null
                                    ? stats.avgReturn >= 0
                                        ? styles.positive
                                        : styles.negative
                                    : ""
                            }`}>
                            {formatPercent(stats.avgReturn)}
                        </span>
                        <span className={styles.statLabel}>Avg Return</span>
                    </div>
                    <div className={styles.statCard}>
                        <span className={styles.statValue}>
                            {strategies?.length || 0}
                        </span>
                        <span className={styles.statLabel}>Strategies</span>
                    </div>
                </section>
            )}

            <section className={styles.filters}>
                <div className={styles.filterRow}>
                    <label className={styles.filterLabel}>
                        Strategy:
                        <select
                            className={styles.select}
                            value={strategyFilter}
                            onChange={(e) => setStrategyFilter(e.target.value)}>
                            <option value="all">All Strategies</option>
                            {strategies?.map((s) => (
                                <option key={s.id} value={s.id.toString()}>
                                    {s.name}
                                </option>
                            ))}
                        </select>
                    </label>
                    <label className={styles.filterLabel}>
                        Status:
                        <select
                            className={styles.select}
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}>
                            <option value="all">All Statuses</option>
                            <option value="completed">Completed</option>
                            <option value="running">Running</option>
                            <option value="pending">Pending</option>
                            <option value="failed">Failed</option>
                        </select>
                    </label>
                </div>
            </section>

            <section className={styles.content}>
                <Card title={`Backtest Runs (${filteredRuns.length})`}>
                    {!isSupabaseConfigured ? (
                        <div className={styles.emptyState}>
                            <div className={styles.icon}>🔌</div>
                            <h3>Supabase Not Configured</h3>
                            <p>
                                Configure your Supabase connection to view
                                backtest results.
                            </p>
                        </div>
                    ) : loading ? (
                        <div className={styles.loading}>
                            Loading backtest runs...
                        </div>
                    ) : error ? (
                        <div className={styles.error}>
                            Error loading backtests: {error.message}
                        </div>
                    ) : filteredRuns.length === 0 ? (
                        <div className={styles.emptyState}>
                            <div className={styles.icon}>📊</div>
                            <h3>No Backtests Found</h3>
                            <p>
                                {runs && runs.length > 0
                                    ? "No backtests match your current filters."
                                    : "Run a backtest using the CLI to see results here."}
                            </p>
                            <p className={styles.hint}>
                                Use the jobs CLI: <code>asx backtest</code>
                            </p>
                        </div>
                    ) : (
                        <div className={styles.tableWrapper}>
                            <table className={styles.table}>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Strategy</th>
                                        <th>Name</th>
                                        <th>Period</th>
                                        <th>Capital</th>
                                        <th>Return</th>
                                        <th>Status</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredRuns.map((run) => (
                                        <BacktestRow key={run.id} run={run} />
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

export default BacktestsPage;
