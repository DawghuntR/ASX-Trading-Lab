import Card from "../components/Card";
import StatusBadge from "../components/StatusBadge";
import { isSupabaseConfigured } from "../lib/supabase";
import styles from "./HomePage.module.css";

function HomePage() {
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
                            <StatusBadge
                                status="unknown"
                                label="No data"
                            />
                        </div>
                        <div className={styles.statusItem}>
                            <span className={styles.statusLabel}>
                                Symbols Tracked
                            </span>
                            <StatusBadge
                                status="unknown"
                                label="--"
                            />
                        </div>
                    </div>
                </Card>
            </section>

            <section className={styles.signalsSection}>
                <h2 className={styles.sectionTitle}>Today&apos;s Top Signals</h2>
                <div className={styles.signalsGrid}>
                    <Card title="Price Movers">
                        <p className={styles.placeholder}>
                            Top price movement signals will appear here once
                            data ingestion is configured.
                        </p>
                    </Card>
                    <Card title="Volatility Spikes">
                        <p className={styles.placeholder}>
                            Volatility spike alerts will appear here once data
                            ingestion is configured.
                        </p>
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
