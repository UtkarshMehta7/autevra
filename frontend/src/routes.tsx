import { lazy, Suspense } from "react";
import { Navigate, Route, Routes } from "react-router";
import * as Site from "./site/pages";
import { SiteLayout } from "./site/SiteLayout";
import { StudioEntry } from "./studio/StudioEntry";
import * as Work from "./workspace/pages";
import { WorkspaceLayout } from "./workspace/WorkspaceLayout";

// The studio (three.js, CAD viewport) loads only when a studio route is opened.
const Studio = lazy(() => import("./studio/Studio").then((m) => ({ default: m.Studio })));

/** Three environments: the public website, the user workspace and the engineering studio. */
export function AppRoutes() {
  return (
    <Routes>
      <Route element={<SiteLayout />}>
        <Route index element={<Site.Home />} />
        <Route path="platform" element={<Site.Platform />} />
        <Route path="platform/cad" element={<Site.PlatformCad />} />
        <Route path="platform/simulation" element={<Site.PlatformSimulation />} />
        <Route path="platform/autonomous-engineering" element={<Site.PlatformAutonomous />} />
        <Route path="domains" element={<Site.Domains />} />
        <Route path="domains/:domainId" element={<Site.DomainDetail />} />
        <Route path="solutions" element={<Site.Solutions />} />
        <Route path="pricing" element={<Site.Pricing />} />
        <Route path="docs" element={<Site.Docs />} />
        <Route path="about" element={<Site.About />} />
        <Route path="contact" element={<Site.Contact />} />
        <Route path="*" element={<Site.NotFound />} />
      </Route>
      <Route path="app" element={<WorkspaceLayout />}>
        <Route index element={<Work.Dashboard />} />
        <Route path="projects" element={<Work.Projects />} />
        <Route path="models" element={<Work.Models />} />
        <Route path="domains" element={<Work.DomainsPage />} />
        <Route path="simulations" element={<Work.Simulations />} />
        <Route path="files" element={<Work.Files />} />
        <Route path="settings" element={<Work.Settings />} />
        <Route path="*" element={<Navigate to="/app" replace />} />
      </Route>
      <Route path="studio" element={<StudioEntry />} />
      <Route path="studio/:projectId" element={<StudioEntry />} />
      <Route path="studio/:projectId/:workspace" element={
        <Suspense fallback={<div className="notice-page"><p>Loading the studio…</p></div>}>
          <Studio />
        </Suspense>
      } />
    </Routes>
  );
}
