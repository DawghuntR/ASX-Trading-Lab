import { useParams, Link } from "react-router-dom";
import Card from "../components/Card";
import styles from "./SymbolPage.module.css";

function SymbolPage() {
    const { symbol } = useParams<{ symbol: string }>();

    return (
        <div className={styles.page}>
            <nav className={styles.breadcrumb}>
                <Link to="/">Dashboard</Link>
                <span className={styles.separator}>/</span>
                <Link to="/signals">Signals</Link>
                <span className={styles.separator}>/</span>
                <span className={styles.current}>{symbol}</span>
            </nav>

            <header className={styles.header}>
                <h1 className={styles.title}>{symbol}</h1>
                <p className={styles.subtitle}>Symbol details and analytics</p>
            </header>

            <div className={styles.grid}>
                <Card title="Price History">
                    <div className={styles.emptyState}>
                        <p>No price data available.</p>
                        <p className={styles.hint}>
                            Historical price data will appear here after data
                            ingestion.
                        </p>
                    </div>
                </Card>

                <Card title="Recent Signals">
                    <div className={styles.emptyState}>
                        <p>No signals for this symbol.</p>
                    </div>
                </Card>

                <Card title="Company Info">
                    <div className={styles.infoGrid}>
                        <div className={styles.infoItem}>
                            <span className={styles.infoLabel}>Name</span>
                            <span className={styles.infoValue}>--</span>
                        </div>
                        <div className={styles.infoItem}>
                            <span className={styles.infoLabel}>Sector</span>
                            <span className={styles.infoValue}>--</span>
                        </div>
                        <div className={styles.infoItem}>
                            <span className={styles.infoLabel}>Market Cap</span>
                            <span className={styles.infoValue}>--</span>
                        </div>
                    </div>
                </Card>

                <Card title="Announcements">
                    <div className={styles.emptyState}>
                        <p>No recent announcements.</p>
                    </div>
                </Card>
            </div>
        </div>
    );
}

export default SymbolPage;
