import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";
import { BackendWaking } from "./BackendWaking";
import { AppRoutes } from "./routes";
import "./styles.css";
import "./site.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <BackendWaking />
      <AppRoutes />
    </BrowserRouter>
  </StrictMode>,
);
