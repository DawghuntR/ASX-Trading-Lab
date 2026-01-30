import Card from "../components/Card";
import styles from "./PortfolioPage.module.css";

function PortfolioPage() {
    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>Portfolio</h1>
                <p className={styles.subtitle}>
                    Paper trading portfolio and risk metrics
                </p>
            </header>

            <div className={styles.grid}>
                <Card title="Portfolio Summary">
                    <div className={styles.metricsGrid}>
                        <div className={styles.metric}>
                            <span className={styles.metricLabel}>
                                Total Value
                            </span>
                            <span className={styles.metricValue}>--</span>
                        </div>
                        <div className={styles.metric}>
                            <span className={styles.metricLabel}>
                                Daily P&L
                            </span>
                            <span className={styles.metricValue}>--</span>
                        </div>
                        <div className={styles.metric}>
                            <span className={styles.metricLabel}>
                                Open Positions
                            </span>
                            <span className={styles.metricValue}>--</span>
                        </div>
                    </div>
                </Card>

                <Card title="Risk Metrics">
                    <div className={styles.metricsGrid}>
                        <div className={styles.metric}>
                            <span className={styles.metricLabel}>
                                Max Drawdown
                            </span>
                            <span className={styles.metricValue}>--</span>
                        </div>
                        <div className={styles.metric}>
                            <span className={styles.metricLabel}>
                                Sharpe Ratio
                            </span>
                            <span className={styles.metricValue}>--</span>
                        </div>
                        <div className={styles.metric}>
                            <span className={styles.metricLabel}>Win Rate</span>
                            <span className={styles.metricValue}>--</span>
                        </div>
                    </div>
                </Card>
            </div>

            <section className={styles.positions}>
                <Card title="Current Positions">
                    <div className={styles.emptyState}>
                        <p>No open positions.</p>
                        <p className={styles.hint}>
                            Paper trading positions will appear here once the
                            trading ledger is configured (Feature 026).
                        </p>
                    </div>
                </Card>
            </section>

            <section className={styles.history}>
                <Card title="Trade History">
                    <div className={styles.emptyState}>
                        <p>No trade history.</p>
                    </div>
                </Card>
            </section>
        </div>
    );
}

export default PortfolioPage;
