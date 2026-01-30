import { Link } from "react-router-dom";
import Card from "../components/Card";
import StatusBadge from "../components/StatusBadge";
import {
    useJobRunStats,
    useDataQualityIssues,
    useSystemHealth,
} from "../hooks/useObservability";
import styles from "./HealthPage.module.css";

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
        hour: "2-digit",
        minute: "2-digit",
    });
}

function formatDuration(seconds: number | null | undefined): string {
    if (seconds === null || seconds === undefined) return "--";
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds.toFixed(0)}s`;
}

function formatPercentage(value: number | null | undefined): string {
    if (value === null || value === undefined) return "--";
    return `${value.toFixed(1)}%`;
}

function getJobStatusBadge(status: "success" | "partial_failure" | "failure"): "healthy" | "warning" | "error" {
    switch (status) {
        case "success":
            return "healthy";
        case "partial_failure":
            return "warning";
        case "failure":
            return "error";
        default:
            return "error";
    }
}

function getSeverityBadge(severity: "info" | "warning" | "error"): "healthy" | "warning" | "error" {
    switch (severity) {
        case "info":
            return "healthy";
        case "warning":
            return "warning";
        case "error":
            return "error";
        default:
            return "error";
    }
}

function formatJobName(jobName: string): string {
    return jobName
        .split("_")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
}

function HealthPage() {
    const { data: systemHealth, loading: healthLoading } = useSystemHealth();
    const { data: jobStats, loading: statsLoading } = useJobRunStats(30);
    const { data: qualityIssues, loading: issuesLoading } = useDataQualityIssues(50);

    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>System Health</h1>
                <p className={styles.subtitle}>
                    Job execution and data quality monitoring
                </p>
            </header>

            {/* System Health Summary */}
            <section className={styles.summarySection}>
                <Card title="System Health Summary">
                    {healthLoading ? (
                        <p className={styles.loading}>Loading health status...</p>
                    ) : systemHealth ? (
                        <div className={styles.healthGrid}>
                            <div className={styles.healthItem}>
                                <span className={styles.healthLabel}>
                                    Last Successful Run
                                </span>
                                <StatusBadge
                                    status={systemHealth.healthStatus}
                                    label={formatDate(systemHealth.lastSuccessfulRun)}
                                />
                            </div>
                            <div className={styles.healthItem}>
                                <span className={styles.healthLabel}>
                                    Days Since Update
                                </span>
                                <StatusBadge
                                    status={
                                        systemHealth.daysSinceUpdate === 0
                                            ? "healthy"
                                            : systemHealth.daysSinceUpdate <= 1
                                            ? "warning"
                                            : "error"
                                    }
                                    label={formatNumber(systemHealth.daysSinceUpdate)}
                                />
                            </div>
                            <div className={styles.healthItem}>
                                <span className={styles.healthLabel}>
                                    Unresolved Issues
                                </span>
                                <StatusBadge
                                    status={
                                        systemHealth.unresolvedIssueCount === 0
                                            ? "healthy"
                                            : systemHealth.unresolvedIssueCount <= 5
                                            ? "warning"
                                            : "error"
                                    }
                                    label={formatNumber(systemHealth.unresolvedIssueCount)}
                                />
                            </div>
                            <div className={styles.healthItem}>
                                <span className={styles.healthLabel}>
                                    Recent Job Failures (7d)
                                </span>
                                <StatusBadge
                                    status={
                                        systemHealth.recentJobFailures === 0
                                            ? "healthy"
                                            : systemHealth.recentJobFailures <= 3
                                            ? "warning"
                                            : "error"
                                    }
                                    label={formatNumber(systemHealth.recentJobFailures)}
                                />
                            </div>
                            <div className={styles.healthItem}>
                                <span className={styles.healthLabel}>
                                    Overall Health Status
                                </span>
                                <StatusBadge
                                    status={systemHealth.healthStatus}
                                    label={systemHealth.healthStatus.toUpperCase()}
                                />
                            </div>
                        </div>
                    ) : (
                        <p className={styles.placeholder}>
                            Unable to load system health summary.
                        </p>
                    )}
                </Card>
            </section>

            {/* Job Run Statistics */}
            <section className={styles.statsSection}>
                <h2 className={styles.sectionTitle}>Job Run Statistics (30 days)</h2>
                {statsLoading ? (
                    <p className={styles.loading}>Loading job statistics...</p>
                ) : jobStats && jobStats.length > 0 ? (
                    <div className={styles.jobStatsGrid}>
                        {jobStats.map((job) => (
                            <Card key={job.job_name} className={styles.jobCard}>
                                <div className={styles.jobCardHeader}>
                                    <h3 className={styles.jobName}>
                                        {formatJobName(job.job_name)}
                                    </h3>
                                    <StatusBadge
                                        status={getJobStatusBadge(job.last_run_status)}
                                        label={job.last_run_status.replace("_", " ").toUpperCase()}
                                    />
                                </div>
                                <div className={styles.jobMetrics}>
                                    <div className={styles.metric}>
                                        <span className={styles.metricLabel}>
                                            Success Rate
                                        </span>
                                        <span className={styles.metricValue}>
                                            {formatPercentage(job.success_rate)}
                                        </span>
                                    </div>
                                    <div className={styles.metric}>
                                        <span className={styles.metricLabel}>
                                            Total Runs
                                        </span>
                                        <span className={styles.metricValue}>
                                            {formatNumber(job.total_runs)}
                                        </span>
                                    </div>
                                    <div className={styles.metric}>
                                        <span className={styles.metricLabel}>
                                            Successful
                                        </span>
                                        <span className={styles.metricValue}>
                                            {formatNumber(job.successful_runs)}
                                        </span>
                                    </div>
                                    <div className={styles.metric}>
                                        <span className={styles.metricLabel}>
                                            Failed
                                        </span>
                                        <span className={styles.metricValue}>
                                            {formatNumber(job.failed_runs)}
                                        </span>
                                    </div>
                                    <div className={styles.metric}>
                                        <span className={styles.metricLabel}>
                                            Avg Duration
                                        </span>
                                        <span className={styles.metricValue}>
                                            {formatDuration(job.avg_duration_seconds)}
                                        </span>
                                    </div>
                                    <div className={styles.metric}>
                                        <span className={styles.metricLabel}>
                                            Avg Records
                                        </span>
                                        <span className={styles.metricValue}>
                                            {formatNumber(Math.round(job.avg_records_processed))}
                                        </span>
                                    </div>
                                </div>
                                <div className={styles.lastRun}>
                                    <span className={styles.lastRunLabel}>Last Run:</span>
                                    <span className={styles.lastRunTime}>
                                        {formatDate(job.last_run_at)}
                                    </span>
                                </div>
                            </Card>
                        ))}
                    </div>
                ) : (
                    <Card>
                        <p className={styles.placeholder}>
                            No job runs recorded yet. Jobs will appear here once they start executing.
                        </p>
                    </Card>
                )}
            </section>

            {/* Data Quality Issues */}
            <section className={styles.issuesSection}>
                <h2 className={styles.sectionTitle}>Data Quality Issues</h2>
                {issuesLoading ? (
                    <p className={styles.loading}>Loading quality issues...</p>
                ) : qualityIssues && qualityIssues.length > 0 ? (
                    <Card>
                        <div className={styles.tableWrapper}>
                            <table className={styles.issuesTable}>
                                <thead>
                                    <tr>
                                        <th>Check Type</th>
                                        <th>Severity</th>
                                        <th>Affected Count</th>
                                        <th>Description</th>
                                        <th>Check Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {qualityIssues.map((issue) => (
                                        <tr key={issue.id}>
                                            <td className={styles.checkType}>
                                                {formatJobName(issue.check_type)}
                                            </td>
                                            <td>
                                                <StatusBadge
                                                    status={getSeverityBadge(issue.severity)}
                                                    label={issue.severity.toUpperCase()}
                                                />
                                            </td>
                                            <td className={styles.affectedCount}>
                                                {formatNumber(issue.affected_count)}
                                            </td>
                                            <td className={styles.description}>
                                                {issue.description}
                                                {issue.affected_symbols && issue.affected_symbols.length > 0 && (
                                                    <div className={styles.affectedSymbols}>
                                                        {issue.affected_symbols.slice(0, 5).map((symbol) => (
                                                            <Link
                                                                key={symbol}
                                                                to={`/symbol/${symbol}`}
                                                                className={styles.symbolLink}>
                                                                {symbol}
                                                            </Link>
                                                        ))}
                                                        {issue.affected_symbols.length > 5 && (
                                                            <span className={styles.moreSymbols}>
                                                                +{issue.affected_symbols.length - 5} more
                                                            </span>
                                                        )}
                                                    </div>
                                                )}
                                            </td>
                                            <td className={styles.checkDate}>
                                                {formatDate(issue.check_date)}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </Card>
                ) : (
                    <Card>
                        <p className={styles.placeholderGood}>
                            ✓ No unresolved data quality issues detected. System is healthy!
                        </p>
                    </Card>
                )}
            </section>
        </div>
    );
}

export default HealthPage;
