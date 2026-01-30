import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import SignalsPage from "./pages/SignalsPage";
import SymbolPage from "./pages/SymbolPage";
import BacktestsPage from "./pages/BacktestsPage";
import BacktestDetailPage from "./pages/BacktestDetailPage";
import PortfolioPage from "./pages/PortfolioPage";
import ReactionsPage from "./pages/ReactionsPage";
import HealthPage from "./pages/HealthPage";
import NotFoundPage from "./pages/NotFoundPage";

function App() {
    return (
        <Routes>
            <Route
                path="/"
                element={<Layout />}>
                <Route
                    index
                    element={<HomePage />}
                />
                <Route
                    path="signals"
                    element={<SignalsPage />}
                />
                <Route
                    path="symbol/:symbol"
                    element={<SymbolPage />}
                />
                <Route
                    path="backtests"
                    element={<BacktestsPage />}
                />
                <Route
                    path="backtests/:id"
                    element={<BacktestDetailPage />}
                />
                <Route
                    path="portfolio"
                    element={<PortfolioPage />}
                />
                <Route
                    path="reactions"
                    element={<ReactionsPage />}
                />
                <Route
                    path="health"
                    element={<HealthPage />}
                />
                <Route
                    path="*"
                    element={<NotFoundPage />}
                />
            </Route>
        </Routes>
    );
}

export default App;
