import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import Card from "../components/Card";
import {
    useReactionsByType,
    useReactionSummaryByType,
    useReactionSummaryBySensitivity,
} from "../hooks/useData";
import { isSupabaseConfigured } from "../lib/supabase";
import type { AnnouncementReactionWithInstrument } from "../api/data";
import styles from "./ReactionsPage.module.css";

function formatPercent(value: number | null | undefined): string {
    if (value == null) return "--";
    const sign = value >= 0 ? "+" : "";
    return `${sign}${value.toFixed(2)}%`;
}

function formatDate(dateStr: string | null): string {
    if (!dateStr) return "--";
    return new Date(dateStr).toLocaleDateString("en-AU", {
        day: "2-digit",
        month: "short",
        year: "numeric",
    });
}

function SummaryCard({
    title,
    count,
    avgReturn,
    positiveRatio,
}: {
    title: string;
    count: number;
    avgReturn: number;
    positiveRatio: number;
}) {
    const returnClass =
        avgReturn > 0.5
            ? styles.positive
            : avgReturn < -0.5
            ? styles.negative
            : styles.neutral;

    return (
        <div className={styles.summaryCard}>
            <h3 className={styles.summaryTitle}>{title}</h3>
            <div className={styles.summaryStats}>
                <div className={styles.stat}>
                    <span className={styles.statValue}>{count}</span>
                    <span className={styles.statLabel}>Total</span>
                </div>
                <div className={styles.stat}>
                    <span className={`${styles.statValue} ${returnClass}`}>
                        {formatPercent(avgReturn)}
                    </span>
                    <span className={styles.statLabel}>Avg Return</span>
                </div>
                <div className={styles.stat}>
                    <span className={styles.statValue}>
                        {(positiveRatio * 100).toFixed(0)}%
                    </span>
                    <span className={styles.statLabel}>Positive</span>
                </div>
            </div>
        </div>
    );
}

function ReactionRow({
    reaction,
}: {
    reaction: AnnouncementReactionWithInstrument;
}) {
    const directionClass =
        reaction.reaction_direction === "positive"
            ? styles.positive
            : reaction.reaction_direction === "negative"
            ? styles.negative
            : styles.neutral;

    const strengthLabels: Record<string, string> = {
        weak: "Weak",
        medium: "Medium",
        strong: "Strong",
    };

    return (
        <tr className={styles.reactionRow}>
            <td className={styles.symbolCell}>
                <Link
                    to={`/symbol/${reaction.instruments?.symbol || "UNKNOWN"}`}
                    className={styles.symbolLink}>
                    {reaction.instruments?.symbol || "N/A"}
                </Link>
            </td>
            <td className={styles.nameCell}>
                {reaction.instruments?.name || "--"}
            </td>
            <td className={styles.dateCell}>{formatDate(reaction.announcement_date)}</td>
            <td className={styles.typeCell}>
                <span className={styles.typeBadge}>
                    {reaction.document_type || "Unknown"}
                </span>
            </td>
            <td className={styles.sensitivityCell}>
                {reaction.sensitivity || "--"}
            </td>
            <td className={`${styles.returnCell} ${directionClass}`}>
                {formatPercent(reaction.return_1d_pct)}
            </td>
            <td className={`${styles.directionCell} ${directionClass}`}>
                {reaction.reaction_direction || "--"}
            </td>
            <td className={styles.strengthCell}>
                {strengthLabels[reaction.reaction_strength || ""] ||
                    reaction.reaction_strength ||
                    "--"}
            </td>
        </tr>
    );
}

function ReactionsPage() {
    const [documentTypeFilter, setDocumentTypeFilter] = useState<string>("all");
    const [sensitivityFilter, setSensitivityFilter] = useState<string>("all");

    const { data: summaryByType, loading: loadingSummaryByType } =
        useReactionSummaryByType();
    const { data: summaryBySensitivity, loading: loadingSummaryBySensitivity } =
        useReactionSummaryBySensitivity();
    const {
        data: reactions,
        loading: loadingReactions,
        error,
    } = useReactionsByType(
        documentTypeFilter === "all" ? undefined : documentTypeFilter,
        200
    );

    const filteredReactions = useMemo(() => {
        if (!reactions) return [];
        if (sensitivityFilter === "all") return reactions;
        return reactions.filter((r) => r.sensitivity === sensitivityFilter);
    }, [reactions, sensitivityFilter]);

    const documentTypes = useMemo(() => {
        if (!summaryByType) return [];
        return summaryByType.map((s) => s.document_type);
    }, [summaryByType]);

    const sensitivities = useMemo(() => {
        if (!summaryBySensitivity) return [];
        return summaryBySensitivity.map((s) => s.sensitivity);
    }, [summaryBySensitivity]);

    const loading = loadingSummaryByType || loadingSummaryBySensitivity || loadingReactions;

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>News Reactions</h1>
                <p className={styles.subtitle}>
                    1-day price reactions following ASX announcements
                </p>
            </header>

            {!isSupabaseConfigured ? (
                <Card title="Configuration Required">
                    <div className={styles.emptyState}>
                        <h3>Supabase Not Configured</h3>
                        <p>
                            Configure your Supabase connection to view reaction analytics.
                        </p>
                    </div>
                </Card>
            ) : (
                <>
                    <section className={styles.summarySection}>
                        <h2 className={styles.sectionTitle}>Summary by Document Type</h2>
                        {loadingSummaryByType ? (
                            <div className={styles.loading}>Loading summary...</div>
                        ) : summaryByType && summaryByType.length > 0 ? (
                            <div className={styles.summaryGrid}>
                                {summaryByType.slice(0, 8).map((summary) => (
                                    <SummaryCard
                                        key={summary.document_type}
                                        title={summary.document_type}
                                        count={summary.total_count}
                                        avgReturn={summary.avg_return_pct}
                                        positiveRatio={
                                            summary.total_count > 0
                                                ? summary.positive_count / summary.total_count
                                                : 0
                                        }
                                    />
                                ))}
                            </div>
                        ) : (
                            <div className={styles.emptyState}>
                                <p>No reaction data available yet.</p>
                            </div>
                        )}
                    </section>

                    <section className={styles.summarySection}>
                        <h2 className={styles.sectionTitle}>Summary by Sensitivity</h2>
                        {loadingSummaryBySensitivity ? (
                            <div className={styles.loading}>Loading summary...</div>
                        ) : summaryBySensitivity && summaryBySensitivity.length > 0 ? (
                            <div className={styles.summaryGrid}>
                                {summaryBySensitivity.map((summary) => (
                                    <SummaryCard
                                        key={summary.sensitivity}
                                        title={summary.sensitivity}
                                        count={summary.total_count}
                                        avgReturn={summary.avg_return_pct}
                                        positiveRatio={
                                            summary.total_count > 0
                                                ? summary.positive_count / summary.total_count
                                                : 0
                                        }
                                    />
                                ))}
                            </div>
                        ) : (
                            <div className={styles.emptyState}>
                                <p>No sensitivity data available yet.</p>
                            </div>
                        )}
                    </section>

                    <section className={styles.filters}>
                        <div className={styles.filterRow}>
                            <label className={styles.filterLabel}>
                                Document Type:
                                <select
                                    className={styles.select}
                                    value={documentTypeFilter}
                                    onChange={(e) => setDocumentTypeFilter(e.target.value)}>
                                    <option value="all">All Types</option>
                                    {documentTypes.map((type) => (
                                        <option key={type} value={type}>
                                            {type}
                                        </option>
                                    ))}
                                </select>
                            </label>
                            <label className={styles.filterLabel}>
                                Sensitivity:
                                <select
                                    className={styles.select}
                                    value={sensitivityFilter}
                                    onChange={(e) => setSensitivityFilter(e.target.value)}>
                                    <option value="all">All Sensitivities</option>
                                    {sensitivities.map((sens) => (
                                        <option key={sens} value={sens}>
                                            {sens}
                                        </option>
                                    ))}
                                </select>
                            </label>
                        </div>
                    </section>

                    <section className={styles.results}>
                        <Card title={`Recent Reactions (${filteredReactions.length})`}>
                            {loading ? (
                                <div className={styles.loading}>Loading reactions...</div>
                            ) : error ? (
                                <div className={styles.error}>
                                    Error loading reactions: {error.message}
                                </div>
                            ) : filteredReactions.length === 0 ? (
                                <div className={styles.emptyState}>
                                    <h3>No Reactions Found</h3>
                                    <p>
                                        No announcement reactions match the selected filters.
                                    </p>
                                    <p className={styles.hint}>
                                        Reactions are computed by the jobs runner after
                                        announcements are ingested.
                                    </p>
                                </div>
                            ) : (
                                <div className={styles.tableWrapper}>
                                    <table className={styles.table}>
                                        <thead>
                                            <tr>
                                                <th>Symbol</th>
                                                <th>Name</th>
                                                <th>Date</th>
                                                <th>Type</th>
                                                <th>Sensitivity</th>
                                                <th>1D Return</th>
                                                <th>Direction</th>
                                                <th>Strength</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {filteredReactions.map((reaction) => (
                                                <ReactionRow
                                                    key={reaction.id}
                                                    reaction={reaction}
                                                />
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </Card>
                    </section>
                </>
            )}
        </div>
    );
}

export default ReactionsPage;
