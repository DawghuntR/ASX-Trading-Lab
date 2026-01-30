import Card from "../components/Card";
import styles from "./BacktestsPage.module.css";

function BacktestsPage() {
    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>Backtests</h1>
                <p className={styles.subtitle}>
                    Strategy backtesting results and performance analysis
                </p>
            </header>

            <section className={styles.content}>
                <Card title="Backtest Results">
                    <div className={styles.emptyState}>
                        <div className={styles.icon}>📊</div>
                        <h3>No Backtests Yet</h3>
                        <p>
                            Backtest results will appear here once the
                            backtesting engine is configured and strategies have
                            been run.
                        </p>
                        <p className={styles.hint}>
                            See Feature 023 (Backtesting Engine v1) and Feature
                            024 (Strategy Pack v1) for implementation details.
                        </p>
                    </div>
                </Card>
            </section>
        </div>
    );
}

export default BacktestsPage;
