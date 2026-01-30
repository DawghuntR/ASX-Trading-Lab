import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";

const basePath = import.meta.env.BASE_URL;

function handleGitHubPagesRedirect(): void {
    const redirect = sessionStorage.getItem("redirect");
    if (redirect) {
        sessionStorage.removeItem("redirect");
        const relativePath = redirect.replace(basePath, "/");
        if (relativePath !== "/" && relativePath !== window.location.pathname) {
            window.history.replaceState(null, "", relativePath);
        }
    }
}

handleGitHubPagesRedirect();

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <BrowserRouter basename={basePath}>
            <App />
        </BrowserRouter>
    </StrictMode>
);
