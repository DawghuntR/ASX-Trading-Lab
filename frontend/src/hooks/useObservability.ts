/**
 * React hooks for job run tracking and data quality monitoring.
 * Provides easy access to observability data with loading/error states.
 */

import { useState, useEffect, useCallback } from "react";
import {
    getJobRuns,
    getLatestJobRuns,
    getJobRunStats,
    getDataQualityIssues,
    getSystemHealthSummary,
    type JobRun,
    type JobRunStats,
    type DataQualityIssue,
    type SystemHealthSummary,
} from "../api/observability";

interface UseQueryResult<T> {
    data: T | null;
    loading: boolean;
    error: Error | null;
    refetch: () => void;
}

/**
 * Hook for fetching recent job runs.
 * @param days Number of days to look back
 * @param limit Maximum number of records
 */
export function useJobRuns(
    days: number = 30,
    limit: number = 100
): UseQueryResult<JobRun[]> {
    const [data, setData] = useState<JobRun[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getJobRuns(days, limit);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [days, limit]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

/**
 * Hook for fetching the latest run for each job type.
 */
export function useLatestJobRuns(): UseQueryResult<JobRun[]> {
    const [data, setData] = useState<JobRun[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getLatestJobRuns();
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

/**
 * Hook for fetching aggregated job run statistics.
 * @param days Number of days to aggregate
 */
export function useJobRunStats(days: number = 30): UseQueryResult<JobRunStats[]> {
    const [data, setData] = useState<JobRunStats[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getJobRunStats(days);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [days]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

/**
 * Hook for fetching unresolved data quality issues.
 * @param limit Maximum number of issues
 */
export function useDataQualityIssues(
    limit: number = 50
): UseQueryResult<DataQualityIssue[]> {
    const [data, setData] = useState<DataQualityIssue[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getDataQualityIssues(limit);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [limit]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

/**
 * Hook for fetching system health summary.
 */
export function useSystemHealth(): UseQueryResult<SystemHealthSummary> {
    const [data, setData] = useState<SystemHealthSummary | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getSystemHealthSummary();
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}
