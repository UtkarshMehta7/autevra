import { Link, NavLink, Outlet } from "react-router";

const NAV: [string, string][] = [
  ["/app", "Dashboard"], ["/app/projects", "Projects"], ["/app/models", "Models"],
  ["/app/domains", "Domains"], ["/app/simulations", "Simulations"], ["/app/files", "Files"],
  ["/app/settings", "Settings"],
];

export function WorkspaceLayout() {
  return (
    <div className="ws">
      <aside className="ws-side">
        <Link to="/" className="site-brand">AUTEVRA</Link>
        <nav aria-label="Workspace">
          {NAV.map(([to, label]) => <NavLink key={to} to={to} end={to === "/app"}>{label}</NavLink>)}
        </nav>
        <Link to="/studio" className="button primary">Open Studio</Link>
      </aside>
      <main className="ws-main"><Outlet /></main>
    </div>
  );
}
