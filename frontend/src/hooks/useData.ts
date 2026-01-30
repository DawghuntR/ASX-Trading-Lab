/**
 * React hooks for fetching and managing data from Supabase.
 */

import { useState, useEffect, useCallback } from "react";
import {
    getIngestStatus,
    getTodaysSignals,
    getSignalsByDate,
    getInstrumentBySymbol,
    getPriceHistory,
    getSignalsForSymbol,
    getAnnouncementsForSymbol,
    searchInstruments,
    getBacktestRuns,
    getBacktestRunById,
    getStrategies,
    type IngestStatus,
    type SignalWithInstrument,
    type BacktestRunWithStrategy,
    type BacktestDetail,
} from "../api/data";
import type { Database } from "../types/database";

type Instrument = Database["public"]["Tables"]["instruments"]["Row"];
type DailyPrice = Database["public"]["Tables"]["daily_prices"]["Row"];
type Signal = Database["public"]["Tables"]["signals"]["Row"];
type Announcement = Database["public"]["Tables"]["announcements"]["Row"];
type Strategy = Database["public"]["Tables"]["strategies"]["Row"];

interface UseQueryResult<T> {
    data: T | null;
    loading: boolean;
    error: Error | null;
    refetch: () => void;
}

export function useIngestStatus(): UseQueryResult<IngestStatus> {
    const [data, setData] = useState<IngestStatus | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getIngestStatus();
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

export function useTodaysSignals(
    limit: number = 50
): UseQueryResult<SignalWithInstrument[]> {
    const [data, setData] = useState<SignalWithInstrument[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getTodaysSignals(limit);
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

export function useSignalsByDate(
    date: string,
    signalType?: string,
    limit: number = 100
): UseQueryResult<SignalWithInstrument[]> {
    const [data, setData] = useState<SignalWithInstrument[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getSignalsByDate(date, signalType, limit);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [date, signalType, limit]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

export function useInstrument(symbol: string): UseQueryResult<Instrument> {
    const [data, setData] = useState<Instrument | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        if (!symbol) {
            setData(null);
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const result = await getInstrumentBySymbol(symbol);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [symbol]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

export function usePriceHistory(
    symbol: string,
    days: number = 90
): UseQueryResult<DailyPrice[]> {
    const [data, setData] = useState<DailyPrice[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        if (!symbol) {
            setData(null);
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const result = await getPriceHistory(symbol, days);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [symbol, days]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

export function useSymbolSignals(
    symbol: string,
    days: number = 30
): UseQueryResult<Signal[]> {
    const [data, setData] = useState<Signal[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        if (!symbol) {
            setData(null);
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const result = await getSignalsForSymbol(symbol, days);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [symbol, days]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

export function useSymbolAnnouncements(
    symbol: string,
    limit: number = 20
): UseQueryResult<Announcement[]> {
    const [data, setData] = useState<Announcement[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        if (!symbol) {
            setData(null);
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const result = await getAnnouncementsForSymbol(symbol, limit);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [symbol, limit]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

export function useInstrumentSearch(query: string): UseQueryResult<Instrument[]> {
    const [data, setData] = useState<Instrument[] | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        if (!query || query.length < 1) {
            setData([]);
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const result = await searchInstruments(query);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [query]);

    useEffect(() => {
        const debounce = setTimeout(fetch, 300);
        return () => clearTimeout(debounce);
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

export function useBacktestRuns(
    limit: number = 50
): UseQueryResult<BacktestRunWithStrategy[]> {
    const [data, setData] = useState<BacktestRunWithStrategy[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getBacktestRuns(limit);
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

export function useBacktestDetail(
    runId: number | null
): UseQueryResult<BacktestDetail> {
    const [data, setData] = useState<BacktestDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        if (runId === null) {
            setData(null);
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const result = await getBacktestRunById(runId);
            setData(result);
        } catch (e) {
            setError(e instanceof Error ? e : new Error("Unknown error"));
        } finally {
            setLoading(false);
        }
    }, [runId]);

    useEffect(() => {
        fetch();
    }, [fetch]);

    return { data, loading, error, refetch: fetch };
}

export function useStrategies(): UseQueryResult<Strategy[]> {
    const [data, setData] = useState<Strategy[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    const fetch = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getStrategies();
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
