export type Json =
    | string
    | number
    | boolean
    | null
    | { [key: string]: Json | undefined }
    | Json[];

export type SignalType =
    | "price_movement"
    | "volatility_spike"
    | "gap_up"
    | "gap_down"
    | "volume_surge"
    | "breakout"
    | "breakdown"
    | "custom";

export type SignalDirection = "bullish" | "bearish" | "neutral";

export type AnnouncementSensitivity =
    | "price_sensitive"
    | "not_price_sensitive"
    | "unknown";

export type ReactionDirection = "positive" | "negative" | "neutral";

export type ReactionStrength = "weak" | "medium" | "strong";

export type OrderStatus =
    | "pending"
    | "filled"
    | "partial"
    | "cancelled"
    | "rejected";

export type OrderSide = "buy" | "sell";

export type OrderType = "market" | "limit" | "stop" | "stop_limit";

export type JobRunStatus = "success" | "partial_failure" | "failure";

export type DataQualitySeverity = "info" | "warning" | "error";

export interface Database {
    public: {
        Tables: {
            instruments: {
                Row: {
                    id: number;
                    symbol: string;
                    name: string | null;
                    sector: string | null;
                    industry: string | null;
                    market_cap: number | null;
                    is_asx300: boolean;
                    is_active: boolean;
                    listed_date: string | null;
                    delisted_date: string | null;
                    metadata: Json;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id?: number;
                    symbol: string;
                    name?: string | null;
                    sector?: string | null;
                    industry?: string | null;
                    market_cap?: number | null;
                    is_asx300?: boolean;
                    is_active?: boolean;
                    listed_date?: string | null;
                    delisted_date?: string | null;
                    metadata?: Json;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    id?: number;
                    symbol?: string;
                    name?: string | null;
                    sector?: string | null;
                    industry?: string | null;
                    market_cap?: number | null;
                    is_asx300?: boolean;
                    is_active?: boolean;
                    listed_date?: string | null;
                    delisted_date?: string | null;
                    metadata?: Json;
                    created_at?: string;
                    updated_at?: string;
                };
            };
            daily_prices: {
                Row: {
                    id: number;
                    instrument_id: number;
                    trade_date: string;
                    open: number | null;
                    high: number | null;
                    low: number | null;
                    close: number;
                    adjusted_close: number | null;
                    volume: number;
                    turnover: number | null;
                    trades_count: number | null;
                    data_source: string;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    instrument_id: number;
                    trade_date: string;
                    open?: number | null;
                    high?: number | null;
                    low?: number | null;
                    close: number;
                    adjusted_close?: number | null;
                    volume?: number;
                    turnover?: number | null;
                    trades_count?: number | null;
                    data_source?: string;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    instrument_id?: number;
                    trade_date?: string;
                    open?: number | null;
                    high?: number | null;
                    low?: number | null;
                    close?: number;
                    adjusted_close?: number | null;
                    volume?: number;
                    turnover?: number | null;
                    trades_count?: number | null;
                    data_source?: string;
                    created_at?: string;
                };
            };
            midday_snapshots: {
                Row: {
                    id: number;
                    instrument_id: number;
                    snapshot_date: string;
                    snapshot_time: string;
                    price: number;
                    change_from_open: number | null;
                    change_percent: number | null;
                    volume_at_snapshot: number | null;
                    bid: number | null;
                    ask: number | null;
                    data_source: string;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    instrument_id: number;
                    snapshot_date: string;
                    snapshot_time: string;
                    price: number;
                    change_from_open?: number | null;
                    change_percent?: number | null;
                    volume_at_snapshot?: number | null;
                    bid?: number | null;
                    ask?: number | null;
                    data_source?: string;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    instrument_id?: number;
                    snapshot_date?: string;
                    snapshot_time?: string;
                    price?: number;
                    change_from_open?: number | null;
                    change_percent?: number | null;
                    volume_at_snapshot?: number | null;
                    bid?: number | null;
                    ask?: number | null;
                    data_source?: string;
                    created_at?: string;
                };
            };
            signals: {
                Row: {
                    id: number;
                    instrument_id: number;
                    signal_date: string;
                    signal_type: SignalType;
                    signal_direction: SignalDirection;
                    signal_strength: number | null;
                    value: number | null;
                    threshold: number | null;
                    description: string | null;
                    metadata: Json;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    instrument_id: number;
                    signal_date: string;
                    signal_type: SignalType;
                    signal_direction?: SignalDirection;
                    signal_strength?: number | null;
                    value?: number | null;
                    threshold?: number | null;
                    description?: string | null;
                    metadata?: Json;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    instrument_id?: number;
                    signal_date?: string;
                    signal_type?: SignalType;
                    signal_direction?: SignalDirection;
                    signal_strength?: number | null;
                    value?: number | null;
                    threshold?: number | null;
                    description?: string | null;
                    metadata?: Json;
                    created_at?: string;
                };
            };
            announcements: {
                Row: {
                    id: number;
                    instrument_id: number;
                    announced_at: string;
                    headline: string;
                    url: string | null;
                    document_type: string | null;
                    sensitivity: AnnouncementSensitivity;
                    pages: number | null;
                    file_size_kb: number | null;
                    asx_announcement_id: string | null;
                    content_hash: string | null;
                    metadata: Json;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    instrument_id: number;
                    announced_at: string;
                    headline: string;
                    url?: string | null;
                    document_type?: string | null;
                    sensitivity?: AnnouncementSensitivity;
                    pages?: number | null;
                    file_size_kb?: number | null;
                    asx_announcement_id?: string | null;
                    content_hash?: string | null;
                    metadata?: Json;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    instrument_id?: number;
                    announced_at?: string;
                    headline?: string;
                    url?: string | null;
                    document_type?: string | null;
                    sensitivity?: AnnouncementSensitivity;
                    pages?: number | null;
                    file_size_kb?: number | null;
                    asx_announcement_id?: string | null;
                    content_hash?: string | null;
                    metadata?: Json;
                    created_at?: string;
                };
            };
            announcement_reactions: {
                Row: {
                    id: number;
                    announcement_id: number;
                    instrument_id: number;
                    announcement_date: string;
                    announcement_close: number | null;
                    announcement_volume: number | null;
                    next_day_date: string | null;
                    next_day_open: number | null;
                    next_day_close: number | null;
                    next_day_high: number | null;
                    next_day_low: number | null;
                    next_day_volume: number | null;
                    return_1d: number | null;
                    return_1d_pct: number | null;
                    gap_open_pct: number | null;
                    intraday_range_pct: number | null;
                    volume_change_pct: number | null;
                    reaction_direction: ReactionDirection;
                    reaction_strength: ReactionStrength;
                    document_type: string | null;
                    sensitivity: string | null;
                    headline: string;
                    computed_at: string;
                };
                Insert: {
                    id?: number;
                    announcement_id: number;
                    instrument_id: number;
                    announcement_date: string;
                    announcement_close?: number | null;
                    announcement_volume?: number | null;
                    next_day_date?: string | null;
                    next_day_open?: number | null;
                    next_day_close?: number | null;
                    next_day_high?: number | null;
                    next_day_low?: number | null;
                    next_day_volume?: number | null;
                    return_1d?: number | null;
                    return_1d_pct?: number | null;
                    gap_open_pct?: number | null;
                    intraday_range_pct?: number | null;
                    volume_change_pct?: number | null;
                    reaction_direction: ReactionDirection;
                    reaction_strength: ReactionStrength;
                    document_type?: string | null;
                    sensitivity?: string | null;
                    headline: string;
                    computed_at?: string;
                };
                Update: {
                    id?: number;
                    announcement_id?: number;
                    instrument_id?: number;
                    announcement_date?: string;
                    announcement_close?: number | null;
                    announcement_volume?: number | null;
                    next_day_date?: string | null;
                    next_day_open?: number | null;
                    next_day_close?: number | null;
                    next_day_high?: number | null;
                    next_day_low?: number | null;
                    next_day_volume?: number | null;
                    return_1d?: number | null;
                    return_1d_pct?: number | null;
                    gap_open_pct?: number | null;
                    intraday_range_pct?: number | null;
                    volume_change_pct?: number | null;
                    reaction_direction?: ReactionDirection;
                    reaction_strength?: ReactionStrength;
                    document_type?: string | null;
                    sensitivity?: string | null;
                    headline?: string;
                    computed_at?: string;
                };
            };
            strategies: {
                Row: {
                    id: number;
                    name: string;
                    description: string | null;
                    version: string;
                    parameters: Json;
                    is_active: boolean;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id?: number;
                    name: string;
                    description?: string | null;
                    version?: string;
                    parameters?: Json;
                    is_active?: boolean;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    id?: number;
                    name?: string;
                    description?: string | null;
                    version?: string;
                    parameters?: Json;
                    is_active?: boolean;
                    created_at?: string;
                    updated_at?: string;
                };
            };
            backtest_runs: {
                Row: {
                    id: number;
                    strategy_id: number;
                    name: string | null;
                    start_date: string;
                    end_date: string;
                    initial_capital: number;
                    final_capital: number | null;
                    parameters: Json;
                    status: string;
                    started_at: string | null;
                    completed_at: string | null;
                    error_message: string | null;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    strategy_id: number;
                    name?: string | null;
                    start_date: string;
                    end_date: string;
                    initial_capital?: number;
                    final_capital?: number | null;
                    parameters?: Json;
                    status?: string;
                    started_at?: string | null;
                    completed_at?: string | null;
                    error_message?: string | null;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    strategy_id?: number;
                    name?: string | null;
                    start_date?: string;
                    end_date?: string;
                    initial_capital?: number;
                    final_capital?: number | null;
                    parameters?: Json;
                    status?: string;
                    started_at?: string | null;
                    completed_at?: string | null;
                    error_message?: string | null;
                    created_at?: string;
                };
            };
            backtest_metrics: {
                Row: {
                    id: number;
                    backtest_run_id: number;
                    total_return: number | null;
                    annualized_return: number | null;
                    sharpe_ratio: number | null;
                    sortino_ratio: number | null;
                    max_drawdown: number | null;
                    max_drawdown_duration: number | null;
                    win_rate: number | null;
                    profit_factor: number | null;
                    total_trades: number;
                    winning_trades: number;
                    losing_trades: number;
                    avg_win: number | null;
                    avg_loss: number | null;
                    largest_win: number | null;
                    largest_loss: number | null;
                    avg_holding_period_days: number | null;
                    exposure_time: number | null;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    backtest_run_id: number;
                    total_return?: number | null;
                    annualized_return?: number | null;
                    sharpe_ratio?: number | null;
                    sortino_ratio?: number | null;
                    max_drawdown?: number | null;
                    max_drawdown_duration?: number | null;
                    win_rate?: number | null;
                    profit_factor?: number | null;
                    total_trades?: number;
                    winning_trades?: number;
                    losing_trades?: number;
                    avg_win?: number | null;
                    avg_loss?: number | null;
                    largest_win?: number | null;
                    largest_loss?: number | null;
                    avg_holding_period_days?: number | null;
                    exposure_time?: number | null;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    backtest_run_id?: number;
                    total_return?: number | null;
                    annualized_return?: number | null;
                    sharpe_ratio?: number | null;
                    sortino_ratio?: number | null;
                    max_drawdown?: number | null;
                    max_drawdown_duration?: number | null;
                    win_rate?: number | null;
                    profit_factor?: number | null;
                    total_trades?: number;
                    winning_trades?: number;
                    losing_trades?: number;
                    avg_win?: number | null;
                    avg_loss?: number | null;
                    largest_win?: number | null;
                    largest_loss?: number | null;
                    avg_holding_period_days?: number | null;
                    exposure_time?: number | null;
                    created_at?: string;
                };
            };
            backtest_trades: {
                Row: {
                    id: number;
                    backtest_run_id: number;
                    instrument_id: number;
                    entry_date: string;
                    entry_price: number;
                    exit_date: string | null;
                    exit_price: number | null;
                    quantity: number;
                    side: string;
                    pnl: number | null;
                    pnl_percent: number | null;
                    exit_reason: string | null;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    backtest_run_id: number;
                    instrument_id: number;
                    entry_date: string;
                    entry_price: number;
                    exit_date?: string | null;
                    exit_price?: number | null;
                    quantity: number;
                    side: string;
                    pnl?: number | null;
                    pnl_percent?: number | null;
                    exit_reason?: string | null;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    backtest_run_id?: number;
                    instrument_id?: number;
                    entry_date?: string;
                    entry_price?: number;
                    exit_date?: string | null;
                    exit_price?: number | null;
                    quantity?: number;
                    side?: string;
                    pnl?: number | null;
                    pnl_percent?: number | null;
                    exit_reason?: string | null;
                    created_at?: string;
                };
            };
            paper_accounts: {
                Row: {
                    id: number;
                    name: string;
                    initial_balance: number;
                    cash_balance: number;
                    is_active: boolean;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id?: number;
                    name: string;
                    initial_balance?: number;
                    cash_balance?: number;
                    is_active?: boolean;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    id?: number;
                    name?: string;
                    initial_balance?: number;
                    cash_balance?: number;
                    is_active?: boolean;
                    created_at?: string;
                    updated_at?: string;
                };
            };
            paper_orders: {
                Row: {
                    id: number;
                    account_id: number;
                    instrument_id: number;
                    order_side: OrderSide;
                    order_type: OrderType;
                    quantity: number;
                    limit_price: number | null;
                    stop_price: number | null;
                    filled_quantity: number;
                    filled_avg_price: number | null;
                    status: OrderStatus;
                    submitted_at: string;
                    filled_at: string | null;
                    cancelled_at: string | null;
                    notes: string | null;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    account_id: number;
                    instrument_id: number;
                    order_side: OrderSide;
                    order_type?: OrderType;
                    quantity: number;
                    limit_price?: number | null;
                    stop_price?: number | null;
                    filled_quantity?: number;
                    filled_avg_price?: number | null;
                    status?: OrderStatus;
                    submitted_at?: string;
                    filled_at?: string | null;
                    cancelled_at?: string | null;
                    notes?: string | null;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    account_id?: number;
                    instrument_id?: number;
                    order_side?: OrderSide;
                    order_type?: OrderType;
                    quantity?: number;
                    limit_price?: number | null;
                    stop_price?: number | null;
                    filled_quantity?: number;
                    filled_avg_price?: number | null;
                    status?: OrderStatus;
                    submitted_at?: string;
                    filled_at?: string | null;
                    cancelled_at?: string | null;
                    notes?: string | null;
                    created_at?: string;
                };
            };
            paper_positions: {
                Row: {
                    id: number;
                    account_id: number;
                    instrument_id: number;
                    quantity: number;
                    avg_entry_price: number;
                    current_price: number | null;
                    unrealized_pnl: number | null;
                    realized_pnl: number;
                    opened_at: string;
                    updated_at: string;
                };
                Insert: {
                    id?: number;
                    account_id: number;
                    instrument_id: number;
                    quantity?: number;
                    avg_entry_price: number;
                    current_price?: number | null;
                    unrealized_pnl?: number | null;
                    realized_pnl?: number;
                    opened_at?: string;
                    updated_at?: string;
                };
                Update: {
                    id?: number;
                    account_id?: number;
                    instrument_id?: number;
                    quantity?: number;
                    avg_entry_price?: number;
                    current_price?: number | null;
                    unrealized_pnl?: number | null;
                    realized_pnl?: number;
                    opened_at?: string;
                    updated_at?: string;
                };
            };
            portfolio_snapshots: {
                Row: {
                    id: number;
                    account_id: number;
                    snapshot_date: string;
                    cash_balance: number;
                    positions_value: number;
                    total_value: number;
                    daily_pnl: number | null;
                    daily_return: number | null;
                    positions_snapshot: Json;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    account_id: number;
                    snapshot_date: string;
                    cash_balance: number;
                    positions_value: number;
                    total_value: number;
                    daily_pnl?: number | null;
                    daily_return?: number | null;
                    positions_snapshot?: Json;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    account_id?: number;
                    snapshot_date?: string;
                    cash_balance?: number;
                    positions_value?: number;
                    total_value?: number;
                    daily_pnl?: number | null;
                    daily_return?: number | null;
                    positions_snapshot?: Json;
                    created_at?: string;
                };
            };
            job_runs: {
                Row: {
                    id: number;
                    job_name: string;
                    run_date: string;
                    started_at: string;
                    completed_at: string;
                    status: JobRunStatus;
                    records_processed: number;
                    records_failed: number;
                    duration_seconds: number | null;
                    error_message: string | null;
                    metadata: Json;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    job_name: string;
                    run_date: string;
                    started_at: string;
                    completed_at: string;
                    status: JobRunStatus;
                    records_processed?: number;
                    records_failed?: number;
                    duration_seconds?: number | null;
                    error_message?: string | null;
                    metadata?: Json;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    job_name?: string;
                    run_date?: string;
                    started_at?: string;
                    completed_at?: string;
                    status?: JobRunStatus;
                    records_processed?: number;
                    records_failed?: number;
                    duration_seconds?: number | null;
                    error_message?: string | null;
                    metadata?: Json;
                    created_at?: string;
                };
            };
            data_quality_checks: {
                Row: {
                    id: number;
                    check_date: string;
                    check_type: string;
                    severity: DataQualitySeverity;
                    affected_count: number;
                    affected_symbols: string[];
                    description: string | null;
                    details: Json;
                    resolved_at: string | null;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    check_date: string;
                    check_type: string;
                    severity: DataQualitySeverity;
                    affected_count?: number;
                    affected_symbols?: string[];
                    description?: string | null;
                    details?: Json;
                    resolved_at?: string | null;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    check_date?: string;
                    check_type?: string;
                    severity?: DataQualitySeverity;
                    affected_count?: number;
                    affected_symbols?: string[];
                    description?: string | null;
                    details?: Json;
                    resolved_at?: string | null;
                    created_at?: string;
                };
            };
        };
        Views: {
            v_latest_prices: {
                Row: {
                    instrument_id: number;
                    symbol: string;
                    name: string | null;
                    sector: string | null;
                    is_asx300: boolean;
                    trade_date: string;
                    open: number | null;
                    high: number | null;
                    low: number | null;
                    close: number;
                    adjusted_close: number | null;
                    volume: number;
                    turnover: number | null;
                    change_percent: number | null;
                };
            };
            v_todays_signals: {
                Row: {
                    symbol: string;
                    name: string | null;
                    signal_date: string;
                    signal_type: SignalType;
                    signal_direction: SignalDirection;
                    signal_strength: number | null;
                    value: number | null;
                    description: string | null;
                    current_price: number | null;
                    volume: number | null;
                };
            };
            v_price_movers: {
                Row: {
                    symbol: string;
                    name: string | null;
                    sector: string | null;
                    trade_date: string;
                    close: number;
                    prev_close: number;
                    change_percent: number;
                };
            };
            v_ingest_health: {
                Row: {
                    data_type: string;
                    latest_date: string | null;
                    instruments_covered: number;
                    total_records: number;
                    last_ingest_at: string | null;
                };
            };
            v_backtest_leaderboard: {
                Row: {
                    strategy_name: string;
                    run_name: string | null;
                    start_date: string;
                    end_date: string;
                    initial_capital: number;
                    final_capital: number | null;
                    total_return: number | null;
                    annualized_return: number | null;
                    sharpe_ratio: number | null;
                    max_drawdown: number | null;
                    win_rate: number | null;
                    total_trades: number | null;
                    completed_at: string | null;
                };
            };
            v_portfolio_summary: {
                Row: {
                    account_id: number;
                    account_name: string;
                    initial_balance: number;
                    cash_balance: number;
                    positions_value: number;
                    total_value: number;
                    total_return_percent: number | null;
                    open_positions: number;
                };
            };
            v_job_run_summary: {
                Row: {
                    job_name: string;
                    run_date: string;
                    status: JobRunStatus;
                    records_processed: number;
                    records_failed: number;
                    duration_seconds: number | null;
                    error_message: string | null;
                    started_at: string;
                    completed_at: string;
                    run_rank: number;
                };
            };
            v_latest_job_runs: {
                Row: {
                    job_name: string;
                    run_date: string;
                    status: JobRunStatus;
                    records_processed: number;
                    records_failed: number;
                    duration_seconds: number | null;
                    error_message: string | null;
                    started_at: string;
                    completed_at: string;
                };
            };
            v_stale_data_check: {
                Row: {
                    id: number;
                    symbol: string;
                    name: string | null;
                    last_price_date: string | null;
                    days_since_update: number | null;
                    staleness_status: string;
                };
            };
            v_price_quality_issues: {
                Row: {
                    symbol: string;
                    name: string | null;
                    trade_date: string;
                    open: number | null;
                    high: number | null;
                    low: number | null;
                    close: number | null;
                    volume: number | null;
                    issue_type: string;
                };
            };
            v_unresolved_quality_issues: {
                Row: {
                    id: number;
                    check_date: string;
                    check_type: string;
                    severity: DataQualitySeverity;
                    affected_count: number;
                    affected_symbols: string[];
                    description: string | null;
                    details: Json;
                    created_at: string;
                };
            };
        };
        Functions: {
            upsert_instrument: {
                Args: {
                    p_symbol: string;
                    p_name?: string;
                    p_sector?: string;
                    p_industry?: string;
                    p_market_cap?: number;
                    p_is_asx300?: boolean;
                    p_metadata?: Json;
                };
                Returns: number;
            };
            upsert_daily_price: {
                Args: {
                    p_instrument_id: number;
                    p_trade_date: string;
                    p_open: number;
                    p_high: number;
                    p_low: number;
                    p_close: number;
                    p_volume?: number;
                    p_adjusted_close?: number;
                    p_data_source?: string;
                };
                Returns: number;
            };
            get_price_history: {
                Args: {
                    p_symbol: string;
                    p_start_date?: string;
                    p_end_date?: string;
                };
                Returns: {
                    trade_date: string;
                    open: number;
                    high: number;
                    low: number;
                    close: number;
                    volume: number;
                    adjusted_close: number;
                }[];
            };
            get_ingest_status: {
                Args: Record<string, never>;
                Returns: {
                    total_instruments: number;
                    active_instruments: number;
                    asx300_instruments: number;
                    latest_price_date: string | null;
                    prices_today: number;
                    signals_today: number;
                    last_successful_run: string | null;
                    days_since_update: number;
                    unresolved_issues: number;
                }[];
            };
            get_job_run_stats: {
                Args: {
                    p_days?: number;
                };
                Returns: {
                    job_name: string;
                    total_runs: number;
                    successful_runs: number;
                    failed_runs: number;
                    success_rate: number;
                    avg_duration_seconds: number;
                    avg_records_processed: number;
                    last_run_at: string;
                    last_run_status: JobRunStatus;
                }[];
            };
            calc_sma: {
                Args: {
                    p_instrument_id: number;
                    p_date: string;
                    p_period?: number;
                };
                Returns: number | null;
            };
        };
        Enums: {
            signal_type: SignalType;
            signal_direction: SignalDirection;
            announcement_sensitivity: AnnouncementSensitivity;
            order_status: OrderStatus;
            order_side: OrderSide;
            order_type: OrderType;
        };
    };
}
