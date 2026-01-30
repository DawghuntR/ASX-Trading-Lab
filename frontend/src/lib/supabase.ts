import { createClient } from "@supabase/supabase-js";
import type { Database } from "../types/database";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

function validateSupabaseConfig(): { url: string; anonKey: string } | null {
    if (!supabaseUrl || !supabaseAnonKey) {
        console.warn(
            "Supabase configuration missing. Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in .env"
        );
        return null;
    }

    if (
        supabaseUrl === "https://your-project.supabase.co" ||
        supabaseAnonKey === "your-anon-key-here"
    ) {
        console.warn(
            "Supabase configuration contains placeholder values. Update .env with real credentials."
        );
        return null;
    }

    return { url: supabaseUrl, anonKey: supabaseAnonKey };
}

const config = validateSupabaseConfig();

export const supabase = config
    ? createClient<Database>(config.url, config.anonKey)
    : null;

export const isSupabaseConfigured = config !== null;
