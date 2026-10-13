import { useEffect } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router";

const NAV: [string, string][] = [
  ["/platform", "Platform"], ["/domains", "Domains"], ["/solutions", "Solutions"],
  ["/pricing", "Pricing"], ["/docs", "Docs"], ["/about", "About"],
];

export function SiteLayout() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo(0, 0); }, [pathname]);
  return (
    <div className="site">
      <header className="site-header">
        <Link to="/" className="site-brand" aria-label="AUTEVRA home">AUTEVRA</Link>
        <nav className="site-nav" aria-label="Main">
          {NAV.map(([to, label]) => <NavLink key={to} to={to}>{label}</NavLink>)}
        </nav>
        <span className="spacer" />
        <Link to="/app" className="site-link">Workspace</Link>
        <Link to="/studio" className="button primary">Open Engineering Studio</Link>
      </header>
      <main className="site-main"><Outlet /></main>
      <footer className="site-footer">
        <div>
          <strong>AUTEVRA</strong> · Intelligent Engineering
          <p className="hint">Local-first engineering software. Simulation results are labelled by
            credibility; nothing is presented as validated without measured data.</p>
        </div>
        <nav aria-label="Footer">
          <Link to="/platform">Platform</Link><Link to="/domains">Domains</Link>
          <Link to="/docs">Docs</Link><Link to="/pricing">Pricing</Link>
          <Link to="/contact">Contact</Link>
        </nav>
      </footer>
    </div>
  );
}
