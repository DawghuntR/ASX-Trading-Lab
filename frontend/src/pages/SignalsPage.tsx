import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import Card from "../components/Card";
import { useSignalsByDate } from "../hooks/useData";
import { isSupabaseConfigured } from "../lib/supabase";
import styles from "./SignalsPage.module.css";

function formatDate(date: Date): string {
    return date.toISOString().split("T")[0];
}

function SignalRow({
    signal,
}: {
    signal: {
        id: number;
        signal_type: string;
        signal_direction: string;
        signal_strength: number | null;
        value: number | null;
        description: string | null;
        instruments: { symbol: string; name: string | null } | null;
    };
}) {
    const directionClass =
        signal.signal_direction === "bullish"
            ? styles.bullish
            : signal.signal_direction === "bearish"
            ? styles.bearish
            : "";

    const typeLabels: Record<string, string> = {
        price_movement: "Price Move",
        volatility_spike: "Volatility",
        momentum: "Momentum",
        volume_spike: "Volume",
        gap_up: "Gap Up",
        gap_down: "Gap Down",
    };

    return (
        <tr className={styles.signalRow}>
            <td className={styles.symbolCell}>
                <Link
                    to={`/symbol/${signal.instruments?.symbol}`}
                    className={styles.symbolLink}>
                    {signal.instruments?.symbol}
                </Link>
            </td>
            <td className={styles.nameCell}>
                {signal.instruments?.name || "--"}
            </td>
            <td className={styles.typeCell}>
                <span className={styles.typeBadge}>
                    {typeLabels[signal.signal_type] || signal.signal_type}
                </span>
            </td>
            <td className={`${styles.directionCell} ${directionClass}`}>
                {signal.signal_direction}
            </td>
            <td className={styles.strengthCell}>
                {signal.signal_strength?.toFixed(1) || "--"}
            </td>
            <td className={styles.descriptionCell}>
                {signal.description || "--"}
            </td>
        </tr>
    );
}

function SignalsPage() {
    const [signalType, setSignalType] = useState("all");
    const [selectedDate, setSelectedDate] = useState(() => formatDate(new Date()));

    const { data: signals, loading, error } = useSignalsByDate(
        selectedDate,
        signalType === "all" ? undefined : signalType
    );

    const sortedSignals = useMemo(() => {
        if (!signals) return [];
        return [...signals].sort((a, b) => {
            const strengthA = a.signal_strength ?? 0;
            const strengthB = b.signal_strength ?? 0;
            return strengthB - strengthA;
        });
    }, [signals]);

    const signalCounts = useMemo(() => {
        if (!signals) return { total: 0, byType: {} as Record<string, number> };
        const byType: Record<string, number> = {};
        signals.forEach((s) => {
            byType[s.signal_type] = (byType[s.signal_type] || 0) + 1;
        });
        return { total: signals.length, byType };
    }, [signals]);

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>Signals</h1>
                <p className={styles.subtitle}>
                    Daily market signals and analytics for ASX stocks
                </p>
            </header>

            <section className={styles.filters}>
                <div className={styles.filterRow}>
                    <label className={styles.filterLabel}>
                        Signal Type:
                        <select
                            className={styles.select}
                            value={signalType}
                            onChange={(e) => setSignalType(e.target.value)}>
                            <option value="all">
                                All Signals ({signalCounts.total})
                            </option>
                            <option value="price_movement">
                                Price Movement (
                                {signalCounts.byType["price_movement"] || 0})
                            </option>
                            <option value="momentum">
                                Momentum ({signalCounts.byType["momentum"] || 0})
                            </option>
                            <option value="volatility_spike">
                                Volatility Spike (
                                {signalCounts.byType["volatility_spike"] || 0})
                            </option>
                            <option value="volume_spike">
                                Volume Spike (
                                {signalCounts.byType["volume_spike"] || 0})
                            </option>
                        </select>
                    </label>
                    <label className={styles.filterLabel}>
                        Date:
                        <input
                            type="date"
                            className={styles.input}
                            value={selectedDate}
                            onChange={(e) => setSelectedDate(e.target.value)}
                            max={formatDate(new Date())}
                        />
                    </label>
                </div>
            </section>

            <section className={styles.results}>
                <Card
                    title={`Signal Results (${sortedSignals.length})`}>
                    {!isSupabaseConfigured ? (
                        <div className={styles.emptyState}>
                            <h3>Supabase Not Configured</h3>
                            <p>
                                Configure your Supabase connection to view
                                signals.
                            </p>
                        </div>
                    ) : loading ? (
                        <div className={styles.loading}>
                            Loading signals...
                        </div>
                    ) : error ? (
                        <div className={styles.error}>
                            Error loading signals: {error.message}
                        </div>
                    ) : sortedSignals.length === 0 ? (
                        <div className={styles.emptyState}>
                            <h3>No Signals Found</h3>
                            <p>No signals for {selectedDate}.</p>
                            <p className={styles.hint}>
                                Signals are generated after the daily jobs
                                runner processes market data.
                            </p>
                        </div>
                    ) : (
                        <div className={styles.tableWrapper}>
                            <table className={styles.table}>
                                <thead>
                                    <tr>
                                        <th>Symbol</th>
                                        <th>Name</th>
                                        <th>Type</th>
                                        <th>Direction</th>
                                        <th>Strength</th>
                                        <th>Description</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {sortedSignals.map((signal) => (
                                        <SignalRow
                                            key={signal.id}
                                            signal={signal}
                                        />
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

export default SignalsPage;
