/**
 * API functions for job run tracking and data quality monitoring.
 * Provides observability into system health and job execution history.
 */

import { supabase, isSupabaseConfigured } from "../lib/supabase";

export interface JobRun {
    id: number;
    job_name: string;
    run_date: string;
    started_at: string;
    completed_at: string;
    status: "success" | "partial_failure" | "failure";
    records_processed: number;
    records_failed: number;
    duration_seconds: number;
    error_message: string | null;
    metadata: Record<string, unknown>;
    created_at: string;
}

export interface DataQualityIssue {
    id: number;
    check_date: string;
    check_type: string;
    severity: "info" | "warning" | "error";
    affected_count: number;
    affected_symbols: string[];
    description: string;
    details: Record<string, unknown>;
    resolved_at: string | null;
    created_at: string;
}

export interface JobRunStats {
    job_name: string;
    total_runs: number;
    successful_runs: number;
    failed_runs: number;
    success_rate: number;
    avg_duration_seconds: number;
    avg_records_processed: number;
    last_run_at: string;
    last_run_status: "success" | "partial_failure" | "failure";
}

/**
 * Fetch recent job runs.
 * @param days Number of days to look back (default: 30)
 * @param limit Maximum number of records (default: 100)
 */
export async function getJobRuns(
    days: number = 30,
    limit: number = 100
): Promise<JobRun[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    const { data, error } = await supabase
        .from("job_runs")
        .select("*")
        .gte("run_date", startDate.toISOString().split("T")[0])
        .order("run_date", { ascending: false })
        .order("started_at", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching job runs:", error);
        return [];
    }

    return (data as JobRun[]) || [];
}

/**
 * Fetch the latest run for each job type.
 */
export async function getLatestJobRuns(): Promise<JobRun[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("v_latest_job_runs")
        .select("*");

    if (error) {
        console.error("Error fetching latest job runs:", error);
        return [];
    }

    return (data as JobRun[]) || [];
}

/**
 * Fetch job run statistics.
 * @param days Number of days to aggregate (default: 30)
 */
export async function getJobRunStats(days: number = 30): Promise<JobRunStats[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    // Use explicit type cast since Supabase types may not include custom functions
    const { data, error } = await supabase.rpc("get_job_run_stats", {
        p_days: days,
    } as unknown as undefined);

    if (error) {
        console.error("Error fetching job run stats:", error);
        return [];
    }

    return (data as JobRunStats[]) || [];
}

/**
 * Fetch unresolved data quality issues.
 * @param limit Maximum number of issues (default: 50)
 */
export async function getDataQualityIssues(
    limit: number = 50
): Promise<DataQualityIssue[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("data_quality_checks")
        .select("*")
        .is("resolved_at", null)
        .order("check_date", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching data quality issues:", error);
        return [];
    }

    return (data as DataQualityIssue[]) || [];
}

/**
 * Fetch all data quality issues (including resolved).
 * @param days Number of days to look back (default: 30)
 * @param limit Maximum number of issues (default: 100)
 */
export async function getAllDataQualityIssues(
    days: number = 30,
    limit: number = 100
): Promise<DataQualityIssue[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    const { data, error } = await supabase
        .from("data_quality_checks")
        .select("*")
        .gte("check_date", startDate.toISOString().split("T")[0])
        .order("check_date", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching all data quality issues:", error);
        return [];
    }

    return (data as DataQualityIssue[]) || [];
}

/**
 * Get symbols with stale data from the database view.
 */
export async function getStaleDataSymbols(): Promise<
    Array<{
        symbol: string;
        name: string;
        last_price_date: string | null;
        days_since_update: number | null;
        staleness_status: string;
    }>
> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("v_stale_data_check")
        .select("symbol, name, last_price_date, days_since_update, staleness_status")
        .in("staleness_status", ["stale", "never"])
        .limit(100);

    if (error) {
        console.error("Error fetching stale data symbols:", error);
        return [];
    }

    return data || [];
}

/**
 * Get the overall system health summary.
 */
export interface SystemHealthSummary {
    lastSuccessfulRun: string | null;
    daysSinceUpdate: number;
    unresolvedIssueCount: number;
    recentJobFailures: number;
    healthStatus: "healthy" | "warning" | "error" | "unknown";
}

export async function getSystemHealthSummary(): Promise<SystemHealthSummary> {
    const defaultSummary: SystemHealthSummary = {
        lastSuccessfulRun: null,
        daysSinceUpdate: 999,
        unresolvedIssueCount: 0,
        recentJobFailures: 0,
        healthStatus: "unknown",
    };

    if (!isSupabaseConfigured || !supabase) return defaultSummary;

    try {
        // Get ingest status which includes last_successful_run
        // Use explicit type cast since Supabase types may not include updated function signature
        const { data: ingestStatus } = await supabase.rpc("get_ingest_status");
        const statusData = ingestStatus as unknown as Array<{
            last_successful_run: string | null;
            days_since_update: number;
            unresolved_issues: number;
        }> | null;
        
        // Get recent job failures (last 7 days)
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
        
        const { data: recentFailures } = await supabase
            .from("job_runs")
            .select("id")
            .eq("status", "failure")
            .gte("run_date", sevenDaysAgo.toISOString().split("T")[0]);

        const lastSuccessfulRun = statusData?.[0]?.last_successful_run || null;
        const daysSinceUpdate = statusData?.[0]?.days_since_update || 999;
        const unresolvedIssueCount = statusData?.[0]?.unresolved_issues || 0;
        const recentJobFailures = recentFailures?.length || 0;

        // Determine health status
        let healthStatus: SystemHealthSummary["healthStatus"] = "healthy";
        if (daysSinceUpdate > 3 || recentJobFailures > 3 || unresolvedIssueCount > 10) {
            healthStatus = "error";
        } else if (daysSinceUpdate > 1 || recentJobFailures > 0 || unresolvedIssueCount > 0) {
            healthStatus = "warning";
        }

        return {
            lastSuccessfulRun,
            daysSinceUpdate,
            unresolvedIssueCount,
            recentJobFailures,
            healthStatus,
        };
    } catch (error) {
        console.error("Error fetching system health summary:", error);
        return defaultSummary;
    }
}
