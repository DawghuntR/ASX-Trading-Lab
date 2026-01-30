import { useParams, Link } from "react-router-dom";
import Card from "../components/Card";
import PriceChart from "../components/PriceChart";
import {
    useInstrument,
    usePriceHistory,
    useSymbolSignals,
    useSymbolAnnouncements,
} from "../hooks/useData";
import styles from "./SymbolPage.module.css";

function formatMarketCap(value: number | null | undefined): string {
    if (!value) return "--";
    if (value >= 1_000_000_000) return `$${(value / 1_000_000_000).toFixed(2)}B`;
    if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(2)}M`;
    if (value >= 1_000) return `$${(value / 1_000).toFixed(2)}K`;
    return `$${value.toFixed(2)}`;
}

function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-AU", {
        day: "numeric",
        month: "short",
        year: "numeric",
    });
}

function formatDateTime(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleString("en-AU", {
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
    });
}

function getSignalTypeColor(signalType: string): string {
    switch (signalType) {
        case "price_up":
        case "momentum_up":
            return styles.signalPositive;
        case "price_down":
        case "momentum_down":
            return styles.signalNegative;
        case "volatility_spike":
        case "volume_spike":
            return styles.signalWarning;
        default:
            return styles.signalNeutral;
    }
}

function formatSignalType(signalType: string): string {
    return signalType
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

function SymbolPage() {
    const { symbol } = useParams<{ symbol: string }>();

    const {
        data: instrument,
        loading: instrumentLoading,
        error: instrumentError,
    } = useInstrument(symbol || "");

    const {
        data: priceHistory,
        loading: priceLoading,
        error: priceError,
    } = usePriceHistory(symbol || "", 90);

    const {
        data: signals,
        loading: signalsLoading,
        error: signalsError,
    } = useSymbolSignals(symbol || "", 30);

    const {
        data: announcements,
        loading: announcementsLoading,
        error: announcementsError,
    } = useSymbolAnnouncements(symbol || "", 10);

    const chartData =
        priceHistory?.map((p) => ({
            date: p.trade_date,
            close: p.close,
            high: p.high,
            low: p.low,
        })) || [];

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
                <p className={styles.subtitle}>
                    {instrumentLoading
                        ? "Loading..."
                        : instrument?.name || "Symbol details and analytics"}
                </p>
            </header>

            <div className={styles.grid}>
                <Card title="Price History (90 Days)" className={styles.chartCard}>
                    {priceLoading ? (
                        <div className={styles.loadingState}>
                            <div className={styles.spinner}></div>
                            <p>Loading price data...</p>
                        </div>
                    ) : priceError ? (
                        <div className={styles.errorState}>
                            <p>Failed to load price data</p>
                            <p className={styles.hint}>{priceError.message}</p>
                        </div>
                    ) : chartData.length === 0 ? (
                        <div className={styles.emptyState}>
                            <p>No price data available.</p>
                            <p className={styles.hint}>
                                Historical price data will appear here after data
                                ingestion.
                            </p>
                        </div>
                    ) : (
                        <PriceChart data={chartData} height={250} />
                    )}
                </Card>

                <Card title="Recent Signals (30 Days)">
                    {signalsLoading ? (
                        <div className={styles.loadingState}>
                            <div className={styles.spinner}></div>
                            <p>Loading signals...</p>
                        </div>
                    ) : signalsError ? (
                        <div className={styles.errorState}>
                            <p>Failed to load signals</p>
                        </div>
                    ) : !signals || signals.length === 0 ? (
                        <div className={styles.emptyState}>
                            <p>No signals for this symbol.</p>
                        </div>
                    ) : (
                        <ul className={styles.signalList}>
                            {signals.slice(0, 10).map((signal) => (
                                <li key={signal.id} className={styles.signalItem}>
                                    <div className={styles.signalHeader}>
                                        <span
                                            className={`${styles.signalType} ${getSignalTypeColor(signal.signal_type)}`}>
                                            {formatSignalType(signal.signal_type)}
                                        </span>
                                        <span className={styles.signalDate}>
                                            {formatDate(signal.signal_date)}
                                        </span>
                                    </div>
                                    {signal.metadata && (
                                        <div className={styles.signalMeta}>
                                            {typeof signal.metadata === "object" &&
                                                Object.entries(
                                                    signal.metadata as Record<string, unknown>
                                                )
                                                    .slice(0, 3)
                                                    .map(([key, value]) => (
                                                        <span
                                                            key={key}
                                                            className={styles.metaItem}>
                                                            {key}:{" "}
                                                            {typeof value === "number"
                                                                ? value.toFixed(2)
                                                                : String(value)}
                                                        </span>
                                                    ))}
                                        </div>
                                    )}
                                </li>
                            ))}
                        </ul>
                    )}
                </Card>

                <Card title="Company Info">
                    {instrumentLoading ? (
                        <div className={styles.loadingState}>
                            <div className={styles.spinner}></div>
                            <p>Loading...</p>
                        </div>
                    ) : instrumentError ? (
                        <div className={styles.errorState}>
                            <p>Failed to load company info</p>
                        </div>
                    ) : (
                        <div className={styles.infoGrid}>
                            <div className={styles.infoItem}>
                                <span className={styles.infoLabel}>Name</span>
                                <span className={styles.infoValue}>
                                    {instrument?.name || "--"}
                                </span>
                            </div>
                            <div className={styles.infoItem}>
                                <span className={styles.infoLabel}>Sector</span>
                                <span className={styles.infoValue}>
                                    {instrument?.sector || "--"}
                                </span>
                            </div>
                            <div className={styles.infoItem}>
                                <span className={styles.infoLabel}>Market Cap</span>
                                <span className={styles.infoValue}>
                                    {formatMarketCap(instrument?.market_cap)}
                                </span>
                            </div>
                            <div className={styles.infoItem}>
                                <span className={styles.infoLabel}>Status</span>
                                <span
                                    className={`${styles.infoValue} ${
                                        instrument?.is_active
                                            ? styles.positive
                                            : styles.negative
                                    }`}>
                                    {instrument?.is_active ? "Active" : "Inactive"}
                                </span>
                            </div>
                        </div>
                    )}
                </Card>

                <Card title="Recent Announcements">
                    {announcementsLoading ? (
                        <div className={styles.loadingState}>
                            <div className={styles.spinner}></div>
                            <p>Loading announcements...</p>
                        </div>
                    ) : announcementsError ? (
                        <div className={styles.errorState}>
                            <p>Failed to load announcements</p>
                        </div>
                    ) : !announcements || announcements.length === 0 ? (
                        <div className={styles.emptyState}>
                            <p>No recent announcements.</p>
                            <p className={styles.hint}>
                                Announcements will appear here once the ASX
                                announcements ingestion is enabled.
                            </p>
                        </div>
                    ) : (
                        <ul className={styles.announcementList}>
                            {announcements.map((ann) => (
                                <li key={ann.id} className={styles.announcementItem}>
                                    <div className={styles.announcementHeader}>
                                        <span className={styles.announcementTitle}>
                                            {ann.headline}
                                        </span>
                                        <span className={styles.announcementDate}>
                                            {formatDateTime(ann.announced_at)}
                                        </span>
                                    </div>
                                    {ann.document_type && (
                                        <span className={styles.announcementCategory}>
                                            {ann.document_type}
                                        </span>
                                    )}
                                </li>
                            ))}
                        </ul>
                    )}
                </Card>
            </div>
        </div>
    );
}

export default SymbolPage;
