import { Link } from "react-router-dom";
import Card from "../components/Card";
import StatusBadge from "../components/StatusBadge";
import { isSupabaseConfigured } from "../lib/supabase";
import { useIngestStatus, useTodaysSignals } from "../hooks/useData";
import styles from "./HomePage.module.css";

function formatNumber(num: number | null | undefined): string {
    if (num === null || num === undefined) return "--";
    return num.toLocaleString();
}

function formatDate(dateStr: string | null | undefined): string {
    if (!dateStr) return "Never";
    const date = new Date(dateStr);
    const now = new Date();
    const diffDays = Math.floor(
        (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
    );

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;

    return date.toLocaleDateString("en-AU", {
        day: "numeric",
        month: "short",
        year: "numeric",
    });
}

function getStatusFromDate(dateStr: string | null | undefined): "healthy" | "warning" | "error" | "unknown" {
    if (!dateStr) return "unknown";
    const date = new Date(dateStr);
    const now = new Date();
    const diffDays = Math.floor(
        (now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
    );

    if (diffDays === 0) return "healthy";
    if (diffDays <= 2) return "warning";
    return "error";
}

function SignalTypeLabel({ type }: { type: string }) {
    const labels: Record<string, string> = {
        price_movement: "Price Move",
        volatility_spike: "Volatility",
        volume_surge: "Volume",
        gap_up: "Gap Up",
        gap_down: "Gap Down",
        breakout: "Breakout",
        breakdown: "Breakdown",
        custom: "Custom",
    };
    return <span className={styles.signalType}>{labels[type] || type}</span>;
}

function HomePage() {
    const { data: ingestStatus, loading: ingestLoading } = useIngestStatus();
    const { data: signals, loading: signalsLoading } = useTodaysSignals(20);

    const priceMovementSignals =
        signals?.filter(
            (s) =>
                s.signal_type === "price_movement" ||
                s.signal_type === "breakout" ||
                s.signal_type === "breakdown"
        ) || [];
    const volatilitySignals =
        signals?.filter(
            (s) =>
                s.signal_type === "volatility_spike" ||
                s.signal_type === "volume_surge" ||
                s.signal_type === "gap_up" ||
                s.signal_type === "gap_down"
        ) || [];

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>Dashboard</h1>
                <p className={styles.subtitle}>
                    ASX market signals and analytics overview
                </p>
            </header>

            <section className={styles.statusSection}>
                <Card title="System Status">
                    <div className={styles.statusGrid}>
                        <div className={styles.statusItem}>
                            <span className={styles.statusLabel}>
                                Supabase Connection
                            </span>
                            <StatusBadge
                                status={
                                    isSupabaseConfigured ? "healthy" : "warning"
                                }
                                label={
                                    isSupabaseConfigured
                                        ? "Connected"
                                        : "Not Configured"
                                }
                            />
                        </div>
                        <div className={styles.statusItem}>
                            <span className={styles.statusLabel}>
                                Last Ingest
                            </span>
                            {ingestLoading ? (
                                <StatusBadge status="unknown" label="Loading..." />
                            ) : (
                                <StatusBadge
                                    status={getStatusFromDate(
                                        ingestStatus?.latest_price_date
                                    )}
                                    label={formatDate(
                                        ingestStatus?.latest_price_date
                                    )}
                                />
                            )}
                        </div>
                        <div className={styles.statusItem}>
                            <span className={styles.statusLabel}>
                                Symbols Tracked
                            </span>
                            <StatusBadge
                                status={
                                    ingestStatus?.active_instruments
                                        ? "healthy"
                                        : "unknown"
                                }
                                label={formatNumber(
                                    ingestStatus?.active_instruments
                                )}
                            />
                        </div>
                        <div className={styles.statusItem}>
                            <span className={styles.statusLabel}>
                                Today&apos;s Signals
                            </span>
                            <StatusBadge
                                status={
                                    ingestStatus?.signals_today
                                        ? "healthy"
                                        : "unknown"
                                }
                                label={formatNumber(ingestStatus?.signals_today)}
                            />
                        </div>
                    </div>
                </Card>
            </section>

            <section className={styles.signalsSection}>
                <h2 className={styles.sectionTitle}>Today&apos;s Top Signals</h2>
                <div className={styles.signalsGrid}>
                    <Card title="Price Movers">
                        {signalsLoading ? (
                            <p className={styles.loading}>Loading signals...</p>
                        ) : priceMovementSignals.length > 0 ? (
                            <ul className={styles.signalList}>
                                {priceMovementSignals.slice(0, 10).map((signal) => (
                                    <li
                                        key={signal.id}
                                        className={styles.signalItem}>
                                        <Link
                                            to={`/symbol/${signal.instruments?.symbol}`}
                                            className={styles.signalLink}>
                                            <span className={styles.signalSymbol}>
                                                {signal.instruments?.symbol}
                                            </span>
                                            <SignalTypeLabel
                                                type={signal.signal_type}
                                            />
                                            <span
                                                className={`${styles.signalDirection} ${
                                                    signal.signal_direction ===
                                                    "bullish"
                                                        ? styles.bullish
                                                        : signal.signal_direction ===
                                                          "bearish"
                                                        ? styles.bearish
                                                        : ""
                                                }`}>
                                                {signal.signal_direction}
                                            </span>
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className={styles.placeholder}>
                                No price movement signals today.
                            </p>
                        )}
                        {priceMovementSignals.length > 0 && (
                            <Link to="/signals" className={styles.viewAll}>
                                View all signals →
                            </Link>
                        )}
                    </Card>
                    <Card title="Volatility & Volume">
                        {signalsLoading ? (
                            <p className={styles.loading}>Loading signals...</p>
                        ) : volatilitySignals.length > 0 ? (
                            <ul className={styles.signalList}>
                                {volatilitySignals.slice(0, 10).map((signal) => (
                                    <li
                                        key={signal.id}
                                        className={styles.signalItem}>
                                        <Link
                                            to={`/symbol/${signal.instruments?.symbol}`}
                                            className={styles.signalLink}>
                                            <span className={styles.signalSymbol}>
                                                {signal.instruments?.symbol}
                                            </span>
                                            <SignalTypeLabel
                                                type={signal.signal_type}
                                            />
                                            <span className={styles.signalStrength}>
                                                {signal.signal_strength
                                                    ? `${signal.signal_strength.toFixed(1)}x`
                                                    : ""}
                                            </span>
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className={styles.placeholder}>
                                No volatility signals today.
                            </p>
                        )}
                        {volatilitySignals.length > 0 && (
                            <Link to="/signals" className={styles.viewAll}>
                                View all signals →
                            </Link>
                        )}
                    </Card>
                </div>
            </section>

            {!isSupabaseConfigured && (
                <section className={styles.setupSection}>
                    <Card title="Setup Required">
                        <div className={styles.setupContent}>
                            <p>
                                To see live data, configure your Supabase
                                connection:
                            </p>
                            <ol className={styles.setupSteps}>
                                <li>
                                    Create a Supabase project at{" "}
                                    <a
                                        href="https://supabase.com"
                                        target="_blank"
                                        rel="noopener noreferrer">
                                        supabase.com
                                    </a>
                                </li>
                                <li>
                                    Copy <code>.env.example</code> to{" "}
                                    <code>.env</code>
                                </li>
                                <li>
                                    Set <code>VITE_SUPABASE_URL</code> and{" "}
                                    <code>VITE_SUPABASE_ANON_KEY</code>
                                </li>
                                <li>Restart the development server</li>
                            </ol>
                        </div>
                    </Card>
                </section>
            )}
        </div>
    );
}

export default HomePage;
