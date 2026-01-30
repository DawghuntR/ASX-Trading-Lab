export type Json =
    | string
    | number
    | boolean
    | null
    | { [key: string]: Json | undefined }
    | Json[];

export interface Database {
    public: {
        Tables: {
            instruments: {
                Row: {
                    id: number;
                    symbol: string;
                    name: string | null;
                    sector: string | null;
                    market_cap: number | null;
                    created_at: string;
                    updated_at: string;
                };
                Insert: {
                    id?: number;
                    symbol: string;
                    name?: string | null;
                    sector?: string | null;
                    market_cap?: number | null;
                    created_at?: string;
                    updated_at?: string;
                };
                Update: {
                    id?: number;
                    symbol?: string;
                    name?: string | null;
                    sector?: string | null;
                    market_cap?: number | null;
                    created_at?: string;
                    updated_at?: string;
                };
            };
            daily_prices: {
                Row: {
                    id: number;
                    instrument_id: number;
                    date: string;
                    open: number;
                    high: number;
                    low: number;
                    close: number;
                    volume: number;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    instrument_id: number;
                    date: string;
                    open: number;
                    high: number;
                    low: number;
                    close: number;
                    volume: number;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    instrument_id?: number;
                    date?: string;
                    open?: number;
                    high?: number;
                    low?: number;
                    close?: number;
                    volume?: number;
                    created_at?: string;
                };
            };
            signals: {
                Row: {
                    id: number;
                    instrument_id: number;
                    signal_type: string;
                    signal_date: string;
                    value: number;
                    metadata: Json | null;
                    created_at: string;
                };
                Insert: {
                    id?: number;
                    instrument_id: number;
                    signal_type: string;
                    signal_date: string;
                    value: number;
                    metadata?: Json | null;
                    created_at?: string;
                };
                Update: {
                    id?: number;
                    instrument_id?: number;
                    signal_type?: string;
                    signal_date?: string;
                    value?: number;
                    metadata?: Json | null;
                    created_at?: string;
                };
            };
        };
        Views: Record<string, never>;
        Functions: Record<string, never>;
        Enums: Record<string, never>;
    };
}
