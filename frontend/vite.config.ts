import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
    plugins: [react()],
    base: process.env.VITE_BASE_PATH || "/ASX-Trading-Lab/",
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    build: {
        outDir: "dist",
        sourcemap: true,
    },
});
