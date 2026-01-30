/**
 * API functions for fetching data from Supabase.
 * All functions handle the case where Supabase is not configured.
 */

import { supabase, isSupabaseConfigured } from "../lib/supabase";
import type { Database } from "../types/database";

type Instrument = Database["public"]["Tables"]["instruments"]["Row"];
type DailyPrice = Database["public"]["Tables"]["daily_prices"]["Row"];
type Signal = Database["public"]["Tables"]["signals"]["Row"];
type Announcement = Database["public"]["Tables"]["announcements"]["Row"];
type AnnouncementReaction = Database["public"]["Tables"]["announcement_reactions"]["Row"];

export interface IngestStatus {
    total_instruments: number;
    active_instruments: number;
    asx300_instruments: number;
    latest_price_date: string | null;
    prices_today: number;
    signals_today: number;
    last_successful_run: string | null;
    days_since_update: number;
    unresolved_issues: number;
}

export interface SignalWithInstrument extends Signal {
    instruments: Pick<Instrument, "symbol" | "name"> | null;
}

export interface PriceWithInstrument extends DailyPrice {
    instruments: Pick<Instrument, "symbol" | "name" | "sector"> | null;
}

export interface AnnouncementWithInstrument extends Announcement {
    instruments: Pick<Instrument, "symbol" | "name"> | null;
}

export interface AnnouncementReactionWithInstrument extends AnnouncementReaction {
    instruments: Pick<Instrument, "symbol" | "name"> | null;
}

export interface ReactionSummaryByType {
    document_type: string;
    total_count: number;
    positive_count: number;
    negative_count: number;
    neutral_count: number;
    avg_return_pct: number;
    median_return_pct?: number;
}

export interface ReactionSummaryBySensitivity {
    sensitivity: string;
    total_count: number;
    positive_count: number;
    negative_count: number;
    neutral_count: number;
    avg_return_pct: number;
}

export async function getIngestStatus(): Promise<IngestStatus | null> {
    if (!isSupabaseConfigured || !supabase) return null;

    const { data, error } = await supabase.rpc("get_ingest_status");

    if (error) {
        console.error("Error fetching ingest status:", error);
        return null;
    }

    return data as IngestStatus;
}

export async function getTodaysSignals(
    limit: number = 50
): Promise<SignalWithInstrument[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const today = new Date().toISOString().split("T")[0];

    const { data, error } = await supabase
        .from("signals")
        .select("*, instruments(symbol, name)")
        .eq("signal_date", today)
        .order("signal_strength", { ascending: false, nullsFirst: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching signals:", error);
        return [];
    }

    return (data as SignalWithInstrument[]) || [];
}

export async function getSignalsByDate(
    date: string,
    signalType?: string,
    limit: number = 100
): Promise<SignalWithInstrument[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    let query = supabase
        .from("signals")
        .select("*, instruments(symbol, name)")
        .eq("signal_date", date)
        .order("signal_strength", { ascending: false, nullsFirst: false })
        .limit(limit);

    if (signalType && signalType !== "all") {
        query = query.eq("signal_type", signalType);
    }

    const { data, error } = await query;

    if (error) {
        console.error("Error fetching signals:", error);
        return [];
    }

    return (data as SignalWithInstrument[]) || [];
}

export async function getTopMovers(
    limit: number = 10
): Promise<PriceWithInstrument[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("daily_prices")
        .select("*, instruments(symbol, name, sector)")
        .order("trade_date", { ascending: false })
        .limit(limit * 10);

    if (error) {
        console.error("Error fetching top movers:", error);
        return [];
    }

    return (data as PriceWithInstrument[]) || [];
}

export async function getInstrumentBySymbol(
    symbol: string
): Promise<Instrument | null> {
    if (!isSupabaseConfigured || !supabase) return null;

    const { data, error } = await supabase
        .from("instruments")
        .select("*")
        .eq("symbol", symbol.toUpperCase())
        .single();

    if (error) {
        console.error("Error fetching instrument:", error);
        return null;
    }

    return data;
}

export async function getPriceHistory(
    symbol: string,
    days: number = 90
): Promise<DailyPrice[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const instrument = await getInstrumentBySymbol(symbol);
    if (!instrument) return [];

    const { data, error } = await supabase
        .from("daily_prices")
        .select("*")
        .eq("instrument_id", instrument.id)
        .order("trade_date", { ascending: false })
        .limit(days);

    if (error) {
        console.error("Error fetching price history:", error);
        return [];
    }

    return data || [];
}

export async function getSignalsForSymbol(
    symbol: string,
    days: number = 30
): Promise<Signal[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const instrument = await getInstrumentBySymbol(symbol);
    if (!instrument) return [];

    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    const { data, error } = await supabase
        .from("signals")
        .select("*")
        .eq("instrument_id", instrument.id)
        .gte("signal_date", startDate.toISOString().split("T")[0])
        .order("signal_date", { ascending: false });

    if (error) {
        console.error("Error fetching signals:", error);
        return [];
    }

    return data || [];
}

export async function getAnnouncementsForSymbol(
    symbol: string,
    limit: number = 20
): Promise<Announcement[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const instrument = await getInstrumentBySymbol(symbol);
    if (!instrument) return [];

    const { data, error } = await supabase
        .from("announcements")
        .select("*")
        .eq("instrument_id", instrument.id)
        .order("announced_at", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching announcements:", error);
        return [];
    }

    return data || [];
}

export async function searchInstruments(
    query: string,
    limit: number = 10
): Promise<Instrument[]> {
    if (!isSupabaseConfigured || !supabase || query.length < 1) return [];

    const { data, error } = await supabase
        .from("instruments")
        .select("*")
        .eq("is_active", true)
        .or(`symbol.ilike.%${query}%,name.ilike.%${query}%`)
        .order("is_asx300", { ascending: false })
        .order("symbol")
        .limit(limit);

    if (error) {
        console.error("Error searching instruments:", error);
        return [];
    }

    return data || [];
}

export async function getLatestPrices(
    limit: number = 50
): Promise<PriceWithInstrument[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data: latestDateResult } = await supabase
        .from("daily_prices")
        .select("trade_date")
        .order("trade_date", { ascending: false })
        .limit(1)
        .single();

    if (!latestDateResult) return [];

    const { data, error } = await supabase
        .from("daily_prices")
        .select("*, instruments(symbol, name, sector)")
        .eq("trade_date", (latestDateResult as { trade_date: string }).trade_date)
        .order("volume", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching latest prices:", error);
        return [];
    }

    return (data as PriceWithInstrument[]) || [];
}

type BacktestRun = Database["public"]["Tables"]["backtest_runs"]["Row"];
type BacktestMetrics = Database["public"]["Tables"]["backtest_metrics"]["Row"];
type BacktestTrade = Database["public"]["Tables"]["backtest_trades"]["Row"];
type Strategy = Database["public"]["Tables"]["strategies"]["Row"];

export interface BacktestRunWithStrategy extends BacktestRun {
    strategies: Pick<Strategy, "name" | "description"> | null;
}

export interface BacktestTradeWithInstrument extends BacktestTrade {
    instruments: Pick<Instrument, "symbol" | "name"> | null;
}

export interface BacktestDetail {
    run: BacktestRunWithStrategy;
    metrics: BacktestMetrics | null;
    trades: BacktestTradeWithInstrument[];
}

export async function getBacktestRuns(
    limit: number = 50
): Promise<BacktestRunWithStrategy[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("backtest_runs")
        .select("*, strategies(name, description)")
        .order("created_at", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching backtest runs:", error);
        return [];
    }

    return (data as BacktestRunWithStrategy[]) || [];
}

export async function getBacktestRunById(
    runId: number
): Promise<BacktestDetail | null> {
    if (!isSupabaseConfigured || !supabase) return null;

    const { data: runData, error: runError } = await supabase
        .from("backtest_runs")
        .select("*, strategies(name, description)")
        .eq("id", runId)
        .single();

    if (runError || !runData) {
        console.error("Error fetching backtest run:", runError);
        return null;
    }

    const { data: metricsData } = await supabase
        .from("backtest_metrics")
        .select("*")
        .eq("backtest_run_id", runId)
        .single();

    const { data: tradesData, error: tradesError } = await supabase
        .from("backtest_trades")
        .select("*, instruments(symbol, name)")
        .eq("backtest_run_id", runId)
        .order("entry_date", { ascending: true });

    if (tradesError) {
        console.error("Error fetching backtest trades:", tradesError);
    }

    return {
        run: runData as BacktestRunWithStrategy,
        metrics: metricsData as BacktestMetrics | null,
        trades: (tradesData as BacktestTradeWithInstrument[]) || [],
    };
}

export async function getBacktestRunsByStrategy(
    strategyId: number,
    limit: number = 20
): Promise<BacktestRunWithStrategy[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("backtest_runs")
        .select("*, strategies(name, description)")
        .eq("strategy_id", strategyId)
        .order("created_at", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching backtest runs:", error);
        return [];
    }

    return (data as BacktestRunWithStrategy[]) || [];
}

export async function getStrategies(): Promise<Strategy[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("strategies")
        .select("*")
        .order("name");

    if (error) {
        console.error("Error fetching strategies:", error);
        return [];
    }

    return data || [];
}

// Paper Trading / Portfolio Types
type PaperAccount = Database["public"]["Tables"]["paper_accounts"]["Row"];
type PaperPosition = Database["public"]["Tables"]["paper_positions"]["Row"];
type PaperOrder = Database["public"]["Tables"]["paper_orders"]["Row"];
type PortfolioSnapshot = Database["public"]["Tables"]["portfolio_snapshots"]["Row"];

export interface PaperPositionWithInstrument extends PaperPosition {
    instruments: Pick<Instrument, "symbol" | "name" | "sector"> | null;
}

export interface PaperOrderWithInstrument extends PaperOrder {
    instruments: Pick<Instrument, "symbol" | "name"> | null;
}

export interface PortfolioSummary {
    account_id: number;
    account_name: string;
    initial_balance: number;
    cash_balance: number;
    positions_value: number;
    total_value: number;
    total_return_percent: number | null;
    open_positions: number;
}

export interface RiskMetrics {
    total_exposure: number;
    cash_reserve_pct: number;
    current_drawdown_pct: number;
    peak_value: number;
    max_position_concentration: number;
    losing_streak: number;
    is_compliant: boolean;
    violations: string[];
}

export async function getPaperAccounts(): Promise<PaperAccount[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("paper_accounts")
        .select("*")
        .eq("is_active", true)
        .order("name");

    if (error) {
        console.error("Error fetching paper accounts:", error);
        return [];
    }

    return data || [];
}

export async function getPortfolioSummary(
    accountId: number
): Promise<PortfolioSummary | null> {
    if (!isSupabaseConfigured || !supabase) return null;

    const { data, error } = await supabase
        .from("v_portfolio_summary")
        .select("*")
        .eq("account_id", accountId)
        .single();

    if (error) {
        console.error("Error fetching portfolio summary:", error);
        return null;
    }

    return data as PortfolioSummary;
}

export async function getPaperPositions(
    accountId: number
): Promise<PaperPositionWithInstrument[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("paper_positions")
        .select("*, instruments(symbol, name, sector)")
        .eq("account_id", accountId)
        .gt("quantity", 0)
        .order("unrealized_pnl", { ascending: false, nullsFirst: false });

    if (error) {
        console.error("Error fetching paper positions:", error);
        return [];
    }

    return (data as PaperPositionWithInstrument[]) || [];
}

export async function getPaperOrders(
    accountId: number,
    status?: string,
    limit: number = 50
): Promise<PaperOrderWithInstrument[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    let query = supabase
        .from("paper_orders")
        .select("*, instruments(symbol, name)")
        .eq("account_id", accountId)
        .order("submitted_at", { ascending: false })
        .limit(limit);

    if (status) {
        query = query.eq("status", status);
    }

    const { data, error } = await query;

    if (error) {
        console.error("Error fetching paper orders:", error);
        return [];
    }

    return (data as PaperOrderWithInstrument[]) || [];
}

export async function getPortfolioSnapshots(
    accountId: number,
    limit: number = 90
): Promise<PortfolioSnapshot[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("portfolio_snapshots")
        .select("*")
        .eq("account_id", accountId)
        .order("snapshot_date", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching portfolio snapshots:", error);
        return [];
    }

    return data || [];
}

export function computeRiskMetrics(
    summary: PortfolioSummary | null,
    snapshots: PortfolioSnapshot[]
): RiskMetrics {
    const defaults: RiskMetrics = {
        total_exposure: 0,
        cash_reserve_pct: 1,
        current_drawdown_pct: 0,
        peak_value: 0,
        max_position_concentration: 0,
        losing_streak: 0,
        is_compliant: true,
        violations: [],
    };

    if (!summary) return defaults;

    const totalValue = summary.total_value || 0;
    const positionsValue = summary.positions_value || 0;
    const cashBalance = summary.cash_balance || 0;

    const totalExposure = totalValue > 0 ? positionsValue / totalValue : 0;
    const cashReservePct = totalValue > 0 ? cashBalance / totalValue : 1;

    let peakValue = summary.initial_balance;
    for (const snap of snapshots) {
        if (snap.total_value > peakValue) {
            peakValue = snap.total_value;
        }
    }
    if (totalValue > peakValue) {
        peakValue = totalValue;
    }

    const currentDrawdownPct =
        peakValue > 0 ? (peakValue - totalValue) / peakValue : 0;

    const violations: string[] = [];
    const MAX_EXPOSURE = 0.95;
    const MIN_CASH_RESERVE = 0.05;
    const MAX_DRAWDOWN = 0.2;

    if (totalExposure > MAX_EXPOSURE) {
        violations.push(
            `Exposure ${(totalExposure * 100).toFixed(1)}% exceeds ${MAX_EXPOSURE * 100}%`
        );
    }
    if (cashReservePct < MIN_CASH_RESERVE) {
        violations.push(
            `Cash reserve ${(cashReservePct * 100).toFixed(1)}% below ${MIN_CASH_RESERVE * 100}%`
        );
    }
    if (currentDrawdownPct > MAX_DRAWDOWN) {
        violations.push(
            `Drawdown ${(currentDrawdownPct * 100).toFixed(1)}% exceeds ${MAX_DRAWDOWN * 100}%`
        );
    }

    return {
        total_exposure: totalExposure,
        cash_reserve_pct: cashReservePct,
        current_drawdown_pct: currentDrawdownPct,
        peak_value: peakValue,
        max_position_concentration: 0,
        losing_streak: 0,
        is_compliant: violations.length === 0,
        violations,
    };
}

// =========================================================================
// Announcement Reactions API (Feature 022)
// =========================================================================

export async function getReactionsByType(
    documentType?: string,
    limit: number = 100
): Promise<AnnouncementReactionWithInstrument[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    let query = supabase
        .from("announcement_reactions")
        .select("*, instruments(symbol, name)")
        .order("announcement_date", { ascending: false })
        .limit(limit);

    if (documentType) {
        query = query.eq("document_type", documentType);
    }

    const { data, error } = await query;

    if (error) {
        console.error("Error fetching reactions:", error);
        return [];
    }

    return (data as AnnouncementReactionWithInstrument[]) || [];
}

export async function getReactionSummaryByType(): Promise<ReactionSummaryByType[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("announcement_reactions")
        .select("document_type, reaction_direction, return_1d_pct");

    if (error) {
        console.error("Error fetching reaction summary:", error);
        return [];
    }

    type ReactionRow = {
        document_type: string | null;
        reaction_direction: string | null;
        return_1d_pct: number | null;
    };

    const typeStats: Record<string, {
        document_type: string;
        total_count: number;
        positive_count: number;
        negative_count: number;
        neutral_count: number;
        returns: number[];
    }> = {};

    for (const row of (data as ReactionRow[]) || []) {
        const docType = row.document_type || "Unknown";
        if (!typeStats[docType]) {
            typeStats[docType] = {
                document_type: docType,
                total_count: 0,
                positive_count: 0,
                negative_count: 0,
                neutral_count: 0,
                returns: [],
            };
        }

        typeStats[docType].total_count++;
        if (row.reaction_direction === "positive") {
            typeStats[docType].positive_count++;
        } else if (row.reaction_direction === "negative") {
            typeStats[docType].negative_count++;
        } else {
            typeStats[docType].neutral_count++;
        }

        if (row.return_1d_pct != null) {
            typeStats[docType].returns.push(row.return_1d_pct);
        }
    }

    const summary: ReactionSummaryByType[] = [];
    for (const stats of Object.values(typeStats)) {
        const returns = stats.returns;
        const avgReturn = returns.length > 0
            ? returns.reduce((a, b) => a + b, 0) / returns.length
            : 0;
        const sortedReturns = [...returns].sort((a, b) => a - b);
        const medianReturn = returns.length > 0
            ? sortedReturns[Math.floor(returns.length / 2)]
            : 0;

        summary.push({
            document_type: stats.document_type,
            total_count: stats.total_count,
            positive_count: stats.positive_count,
            negative_count: stats.negative_count,
            neutral_count: stats.neutral_count,
            avg_return_pct: avgReturn,
            median_return_pct: medianReturn,
        });
    }

    return summary.sort((a, b) => b.total_count - a.total_count);
}

export async function getReactionSummaryBySensitivity(): Promise<ReactionSummaryBySensitivity[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const { data, error } = await supabase
        .from("announcement_reactions")
        .select("sensitivity, reaction_direction, return_1d_pct");

    if (error) {
        console.error("Error fetching reaction summary:", error);
        return [];
    }

    type SensitivityRow = {
        sensitivity: string | null;
        reaction_direction: string | null;
        return_1d_pct: number | null;
    };

    const sensStats: Record<string, {
        sensitivity: string;
        total_count: number;
        positive_count: number;
        negative_count: number;
        neutral_count: number;
        returns: number[];
    }> = {};

    for (const row of (data as SensitivityRow[]) || []) {
        const sensitivity = row.sensitivity || "unknown";
        if (!sensStats[sensitivity]) {
            sensStats[sensitivity] = {
                sensitivity: sensitivity,
                total_count: 0,
                positive_count: 0,
                negative_count: 0,
                neutral_count: 0,
                returns: [],
            };
        }

        sensStats[sensitivity].total_count++;
        if (row.reaction_direction === "positive") {
            sensStats[sensitivity].positive_count++;
        } else if (row.reaction_direction === "negative") {
            sensStats[sensitivity].negative_count++;
        } else {
            sensStats[sensitivity].neutral_count++;
        }

        if (row.return_1d_pct != null) {
            sensStats[sensitivity].returns.push(row.return_1d_pct);
        }
    }

    const summary: ReactionSummaryBySensitivity[] = [];
    for (const stats of Object.values(sensStats)) {
        const returns = stats.returns;
        const avgReturn = returns.length > 0
            ? returns.reduce((a, b) => a + b, 0) / returns.length
            : 0;

        summary.push({
            sensitivity: stats.sensitivity,
            total_count: stats.total_count,
            positive_count: stats.positive_count,
            negative_count: stats.negative_count,
            neutral_count: stats.neutral_count,
            avg_return_pct: avgReturn,
        });
    }

    return summary.sort((a, b) => b.total_count - a.total_count);
}

export async function getReactionsForSymbol(
    symbol: string,
    limit: number = 50
): Promise<AnnouncementReaction[]> {
    if (!isSupabaseConfigured || !supabase) return [];

    const instrument = await getInstrumentBySymbol(symbol);
    if (!instrument) return [];

    const { data, error } = await supabase
        .from("announcement_reactions")
        .select("*")
        .eq("instrument_id", instrument.id)
        .order("announcement_date", { ascending: false })
        .limit(limit);

    if (error) {
        console.error("Error fetching reactions:", error);
        return [];
    }

    return data || [];
}
