import Card from "../components/Card";
import styles from "./SignalsPage.module.css";

function SignalsPage() {
    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>Signals</h1>
                <p className={styles.subtitle}>
                    Daily market signals and analytics for ASX stocks
                </p>
            </header>

            <section className={styles.filters}>
                <Card>
                    <div className={styles.filterRow}>
                        <label className={styles.filterLabel}>
                            Signal Type:
                            <select className={styles.select}>
                                <option value="all">All Signals</option>
                                <option value="price_movement">
                                    Price Movement
                                </option>
                                <option value="volatility">
                                    Volatility Spike
                                </option>
                            </select>
                        </label>
                        <label className={styles.filterLabel}>
                            Date:
                            <input
                                type="date"
                                className={styles.input}
                            />
                        </label>
                    </div>
                </Card>
            </section>

            <section className={styles.results}>
                <Card title="Signal Results">
                    <div className={styles.emptyState}>
                        <p>No signals found.</p>
                        <p className={styles.hint}>
                            Signals will appear here after data ingestion is
                            configured and the jobs runner has processed market
                            data.
                        </p>
                    </div>
                </Card>
            </section>
        </div>
    );
}

export default SignalsPage;
