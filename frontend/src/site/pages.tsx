import { type FormEvent, type ReactNode, useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { api } from "../api/client";
import type { DomainDef } from "../api/types";

// --- shared building blocks ---------------------------------------------------------------

function Section({ title, kicker, children, id }: {
  title?: string; kicker?: string; children: ReactNode; id?: string;
}) {
  return (
    <section className="site-section" id={id}>
      {kicker && <p className="kicker">{kicker}</p>}
      {title && <h2>{title}</h2>}
      {children}
    </section>
  );
}

function Shot({ src, alt, caption }: { src: string; alt: string; caption: string }) {
  return (
    <figure className="shot">
      <img src={src} alt={alt} loading="lazy" />
      <figcaption>{caption}</figcaption>
    </figure>
  );
}

function Cards({ items }: { items: [string, string][] }) {
  return (
    <div className="cards">
      {items.map(([title, text]) => (
        <div key={title} className="card"><h3>{title}</h3><p>{text}</p></div>
      ))}
    </div>
  );
}

const STATUS_LABEL: Record<DomainDef["status"], string> = {
  available: "Available", experimental: "Experimental", in_development: "In development",
  unavailable: "Roadmap only",
};

function useDomains(): DomainDef[] | null {
  const [domains, setDomains] = useState<DomainDef[] | null>(null);
  useEffect(() => { api.domains().then(setDomains).catch(() => setDomains([])); }, []);
  return domains;
}

function StatusBadge({ status }: { status: DomainDef["status"] }) {
  return <span className={`badge-status ${status}`}>{STATUS_LABEL[status]}</span>;
}

// --- pages ----------------------------------------------------------------------------

export function Home() {
  const domains = useDomains();
  return (
    <>
      <section className="hero">
        <h1>One Engineering Platform. Multiple Worlds.</h1>
        <p className="lede">Design, simulate, integrate, and optimize complex engineering systems
          with an AI-native platform built for the next generation of engineering.</p>
        <div className="cta-row">
          <Link to="/platform" className="button primary large">Explore AUTEVRA</Link>
          <Link to="/studio" className="button large">Open Engineering Studio</Link>
        </div>
        <Shot src="/screenshots/studio-design.jpg" alt="The AUTEVRA engineering studio"
          caption="The engineering studio: parametric CAD model, component tree, instructions and test bench (screenshot of this build)." />
      </section>

      <Section kicker="What it is" title="An engineering record you can talk to">
        <p className="narrow">AUTEVRA keeps one authoritative model of a design: parameters,
          parametric CAD geometry, assembly relationships, requirements and every test run with the
          revision it used. Plain-English instructions become validated operations on that model,
          never free-form edits, and every result carries its evidence.</p>
      </Section>

      <Section kicker="Shared engineering core" title="Built once, reused by every domain">
        <Cards items={[
          ["Parameters and units", "Every quantity has a unit and bounds; mixing millimetres and newtons is an error, not a bug."],
          ["Assemblies and interfaces", "Components mate through named interfaces; closed mounts and load paths are checked."],
          ["Revisions and undo", "Every change is a typed command with exact undo and redo; results record the revision they used."],
          ["Tests and evidence", "Component tests with explicit criteria; runs stored with solver, inputs, numerics and credibility."],
          ["Requirements", "Requirements link to parameters, components and the runs that verify them; ReqIF import and export."],
          ["Plugins", "New parameters, components, rules and tests register through a documented plugin API."],
        ]} />
      </Section>

      <Section kicker="Interactive 3D" title="Real, editable geometry">
        <div className="two-col">
          <p>Geometry is built by CadQuery on the Open CASCADE kernel and exported as STEP. Change
            the wheelbase and the body, frame, axles, wheels and dampers that depend on it are
            rebuilt or moved, nothing else. The viewport can play back simulations from the
            solver's own output.</p>
          <Shot src="/screenshots/studio-assembly.jpg" alt="Integration checks" caption="Integration checks with exact clearances measured on the CAD solids." />
        </div>
      </Section>

      <Section kicker="First domain" title="Automotive, end to end">
        <Cards items={[
          ["Specification interview", "Describe the vehicle; impossible targets are flagged with the physics behind them."],
          ["Suspension test bench", "Quarter-car model verified against the exact linear solution."],
          ["Longitudinal performance", "0–100 km/h and braking with traction, load transfer, drag and rolling resistance."],
          ["Diagnosis", "Failures are traced to the parameters that measurably move the margin."],
        ]} />
      </Section>

      <Section kicker="Autonomous engineering" title="Design → Integrate → Simulate → Diagnose → Optimize → Validate">
        <p className="narrow">The engineering loop tests a candidate, diagnoses the first failure,
          takes the smallest rule-checked fix, retests, and stops when everything passes, when no
          admissible fix exists, or at its iteration limit. Nothing changes until you accept.</p>
        <Link to="/platform/autonomous-engineering" className="button">How the loop works</Link>
      </Section>

      <Section kicker="Multi-domain architecture" title="One core, separate domain modules">
        <p className="narrow">Each domain declares what it actually implements. Today only
          automotive is available; the others are on the roadmap and are shown as such.</p>
        <div className="domain-grid">
          {(domains ?? []).map((d) => (
            <Link key={d.id} to={`/domains/${d.id}`} className="domain-tile">
              <strong>{d.name}</strong><StatusBadge status={d.status} />
            </Link>
          ))}
        </div>
      </Section>

      <Section kicker="Simulation and optimisation" title="Scores come from solvers, not predictions">
        <p className="narrow">Optimisation evaluates bounded candidates with the same solvers as
          the test bench, rejects rule-breaking designs before simulating them, re-verifies the
          winner with full numerics and shows trade-offs as a Pareto set.</p>
      </Section>

      <Section kicker="Roadmap" title="What comes next">
        <ol className="roadmap">
          <li>Traceability and requirements ✓</li><li>Specification interview ✓</li>
          <li>Longitudinal performance ✓ and plugin API ✓</li>
          <li>Half-car and full-vehicle dynamics, Magic Formula tyres</li>
          <li>Validation against measured data</li><li>Uncertainty and robustness</li>
          <li>Electrified powertrain energy</li><li>STEP AP242, FMI and SysML v2 exchange</li>
          <li>Further domains, once the shared core supports them reliably</li>
        </ol>
      </Section>

      <section className="cta-band">
        <h2>See it on your own design</h2>
        <div className="cta-row">
          <Link to="/studio" className="button primary large">Open Engineering Studio</Link>
          <Link to="/contact" className="button large">Request early access</Link>
        </div>
      </section>
    </>
  );
}

export function Platform() {
  return (
    <>
      <section className="page-head"><h1>The platform</h1>
        <p className="lede">Three connected environments over one engineering core.</p></section>
      <Section title="Environments">
        <Cards items={[
          ["Website", "This site: what AUTEVRA is and what it can do today."],
          ["Workspace", "Projects, model templates, simulation history, exported files and settings."],
          ["Engineering studio", "Design, assembly, simulation, AI engineering, optimisation, requirements, systems, manufacturing and the digital thread, on one shared model."],
        ]} />
      </Section>
      <Section title="Architecture">
        <ul className="plain narrow">
          <li><strong>Frontend:</strong> React, TypeScript and three.js (rendering only).</li>
          <li><strong>Backend:</strong> Python and FastAPI; SQLite with migrations.</li>
          <li><strong>Geometry:</strong> CadQuery on Open CASCADE, behind one kernel adapter.</li>
          <li><strong>Solvers:</strong> verified in-house models behind a solver interface; heavier solvers (Project Chrono, FEA, CFD) are evaluated before integration.</li>
          <li><strong>AI:</strong> a deterministic parser first; an optional local model (no hosted inference) only proposes schema-checked operations.</li>
        </ul>
        <p><Link to="/platform/cad">CAD</Link> · <Link to="/platform/simulation">Simulation</Link> ·{" "}
          <Link to="/platform/autonomous-engineering">Autonomous engineering</Link></p>
      </Section>
    </>
  );
}

export function PlatformCad() {
  return (
    <>
      <section className="page-head"><h1>Parametric 3D design</h1>
        <p className="lede">Editable B-rep geometry, not a visual approximation.</p></section>
      <Section title="What works today">
        <ul className="plain narrow">
          <li>Parametric components: body with wheel wells, ladder frame, beam axles, wheels, coil-over dampers (plus plugin components such as brake discs).</li>
          <li>Assembly by mates between named interfaces; dependency graph decides what to rebuild or move.</li>
          <li>Exact clearance checks between placed solids; interference rules for packaging.</li>
          <li>STEP AP214 export with one named, coloured, placed solid per component.</li>
          <li>Undo and redo of every change; geometry cached by its inputs.</li>
        </ul>
      </Section>
      <Section title="Not available yet">
        <p className="narrow">Sketch-based modelling, freeform surfacing, sheet metal, drawings
          with tolerances, CAD import and transform gizmos are on the roadmap.</p>
      </Section>
    </>
  );
}

export function PlatformSimulation() {
  return (
    <>
      <section className="page-head"><h1>Simulation</h1>
        <p className="lede">Every result says how it was obtained and how far to trust it.</p></section>
      <Section title="Solvers in this build">
        <table className="site-table">
          <thead><tr><th>Model</th><th>Credibility</th><th>Verified against</th></tr></thead>
          <tbody>
            <tr><td>Quarter-car ride (step, road hump, pothole)</td><td>Numerical simulation</td><td>Exact linear solution, characteristic equation</td></tr>
            <tr><td>Ride modes</td><td>Analytical estimate</td><td>Closed-form 2-DOF eigenvalues</td></tr>
            <tr><td>Longitudinal (0–100 km/h, braking dry/wet)</td><td>Numerical simulation</td><td>Energy balance, traction formula, v²/(2μg)</td></tr>
            <tr><td>Brake disc heating (plugin)</td><td>Analytical estimate</td><td>Energy balance</td></tr>
          </tbody>
        </table>
        <p className="narrow">No result is labelled experimentally validated: that needs measured
          test data and a correlation, which is planned. Project Chrono, FEA and CFD are on the
          roadmap and will run as separate processes once evaluated.</p>
      </Section>
    </>
  );
}

export function PlatformAutonomous() {
  return (
    <>
      <section className="page-head"><h1>Autonomous engineering</h1>
        <p className="lede">Interpret → Propose → Validate → Modify → Simulate → Evaluate → Diagnose → Optimize → Retest.</p></section>
      <Section title="How it stays trustworthy">
        <Cards items={[
          ["Validated operations", "Instructions become typed commands checked against every design rule before anything changes."],
          ["Dependency intelligence", "A change marks exactly the tests whose inputs it touches as stale; only those rerun."],
          ["Evidence-based diagnosis", "Each input is moved ±10 % and the scenario re-simulated; causes are ranked by measured effect."],
          ["Bounded optimisation", "Seeded search within bounds and a budget; candidates scored only by solver output."],
          ["Approval", "Optimised or looped designs are proposals; accepting one is a single undoable command."],
        ]} />
      </Section>
    </>
  );
}

export function Domains() {
  const domains = useDomains();
  return (
    <>
      <section className="page-head"><h1>Engineering domains</h1>
        <p className="lede">Status comes from the platform's domain registry, not from marketing.</p></section>
      <Section>
        <div className="domain-list">
          {domains === null && <p className="hint">Loading…</p>}
          {(domains ?? []).map((d) => (
            <Link key={d.id} to={`/domains/${d.id}`} className="domain-row">
              <div><strong>{d.name}</strong><p className="hint">{d.description}</p></div>
              <StatusBadge status={d.status} />
            </Link>
          ))}
        </div>
      </Section>
    </>
  );
}

export function DomainDetail() {
  const { domainId } = useParams();
  const domains = useDomains();
  const d = domains?.find((x) => x.id === domainId);
  if (domains && !d) return <NotFound />;
  if (!d) return <p className="hint site-section">Loading…</p>;
  const list = (title: string, items: string[]) => items.length > 0 && (
    <div><h3>{title}</h3><ul className="plain">{items.map((i) => <li key={i}>{i}</li>)}</ul></div>
  );
  return (
    <>
      <section className="page-head"><h1>{d.name}</h1><p className="lede">{d.description}</p>
        <StatusBadge status={d.status} /> <span className="hint">{d.evidence}</span></section>
      <Section>
        <div className="cols">
          {list("Component library", d.component_library)}
          {list("Engineering operations", d.operations)}
          {list("Simulations", d.simulations)}
          {list("Formats", d.formats)}
          {list(d.status === "available" ? "Next" : "Planned", d.roadmap)}
        </div>
        {d.status === "available"
          ? <Link to="/studio" className="button primary">Open the studio</Link>
          : <p className="narrow">Nothing in this domain can be used yet. It will be added once the
              shared core supports its geometry, physics and validation reliably.</p>}
      </Section>
    </>
  );
}

export function Solutions() {
  return (
    <>
      <section className="page-head"><h1>Solutions</h1><p className="lede">Who the current build is useful for.</p></section>
      <Section>
        <Cards items={[
          ["Engineering teams", "Early concept trade studies with traceable requirements and stored evidence."],
          ["EV start-ups", "Specification checks (acceleration bound, battery mass share) and quick packaging studies."],
          ["Research labs and teaching", "Verified reference models, open data formats and a plugin API for new models."],
          ["Component developers", "Package a component as a plugin with its rules, clearances and tests."],
        ]} />
        <p className="narrow hint">AUTEVRA is a prototype: use it for concept work and education,
          not for certification, homologation or production release.</p>
      </Section>
    </>
  );
}

const TIERS: { name: string; price: string; points: string[] }[] = [
  { name: "Community", price: "Free", points: ["Local install", "Automotive domain", "Plugin API"] },
  { name: "Creator", price: "To be announced", points: ["Everything in Community", "Project sharing (planned)"] },
  { name: "Professional", price: "₹9,999 / month (target)", points: ["Everything in Creator", "Team workspaces (planned)", "Priority support (planned)"] },
  { name: "Enterprise", price: "Contact us", points: ["On-premise deployment", "Custom domains and plugins"] },
];

export function Pricing() {
  return (
    <>
      <section className="page-head"><h1>Pricing</h1>
        <p className="lede">Proposed tiers. There is no payment system in this build, so nothing can be purchased yet.</p></section>
      <Section>
        <div className="tiers">
          {TIERS.map((t) => (
            <div key={t.name} className="tier">
              <h3>{t.name}</h3><p className="price">{t.price}</p>
              <ul className="plain">{t.points.map((p) => <li key={p}>{p}</li>)}</ul>
              <Link to="/contact" className="button">Request early access</Link>
            </div>
          ))}
        </div>
      </Section>
    </>
  );
}

const DOCS: [string, ReactNode][] = [
  ["Installation", <>Mac (Apple silicon): <code>make setup</code>, then <code>make dev</code>; open <code>http://localhost:5173</code>. Optional local model: <code>brew install ollama</code>, <code>ollama pull qwen3:1.7b</code>.</>],
  ["Projects", <>Create, open, rename, duplicate and delete projects in the <Link to="/app/projects">workspace</Link>. Each project keeps its full change history.</>],
  ["3D interaction", "Drag to orbit, right-drag to pan, scroll to zoom; click a part to select it; X-ray shows parts inside the body."],
  ["Editing components", "Type values in the parameter editor or give instructions such as “increase the wheelbase by 100 mm”. Rule violations are rejected and the design is unchanged."],
  ["AI operations", "The parser handles parameter changes, previews (“what if …”), tests, diagnosis, optimisation, requirements and specifications. A local model proposes changes for anything else; you confirm or reject."],
  ["Simulations", "Run tests in the Simulation workspace. Each run stores the solver, inputs, numerics, criteria and the exact design revision; “Play in 3D” animates the solver output."],
  ["Plugins", <>See <code>docs/EXTENDING.md</code> in the repository: parameters, components, rules, clearances and tests in one plugin.</>],
  ["Troubleshooting", "If the page reports “Unexpected token <”, restart make dev (the Vite proxy). If the backend is unreachable, check port 8000."],
];

export function Docs() {
  return (
    <>
      <section className="page-head"><h1>Documentation</h1></section>
      <Section>
        <div className="docs">{DOCS.map(([t, body]) => <div key={t}><h3>{t}</h3><p>{body}</p></div>)}</div>
      </Section>
    </>
  );
}

export function About() {
  return (
    <>
      <section className="page-head"><h1>About</h1></section>
      <Section>
        <p className="narrow">AUTEVRA is an independent project building AI-native engineering
          software that a single engineer can run locally. The principles: real, editable
          geometry; operations that are validated before they apply; results that carry their
          evidence and credibility; and no claim that the software cannot back up.</p>
        <p className="narrow hint">There are no partnerships, customers or certifications to
          report.</p>
      </Section>
    </>
  );
}

export function Contact() {
  const [form, setForm] = useState({ name: "", email: "", topic: "early_access", message: "" });
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const submit = (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    api.contact(form).then((r) => setResult(r.note)).catch((x) => setError((x as Error).message));
  };
  return (
    <>
      <section className="page-head"><h1>Contact and early access</h1>
        <p className="lede">Development build: messages are stored in the local database; no e-mail is sent.</p></section>
      <Section>
        {result ? <p className="notice">{result}</p> : (
          <form className="site-form" onSubmit={submit}>
            <label>Name<input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>
            <label>E-mail<input required type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
            <label>Topic<select value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value })}>
              <option value="early_access">Early access</option><option value="question">Question</option>
              <option value="partnership">Partnership</option><option value="other">Other</option>
            </select></label>
            <label>Message<textarea required rows={5} value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} /></label>
            {error && <p className="bad-text">{error}</p>}
            <button className="primary" type="submit">Send</button>
          </form>
        )}
      </Section>
    </>
  );
}

export function NotFound() {
  return (
    <section className="page-head"><h1>Page not found</h1>
      <p><Link to="/" className="button">Back to the home page</Link></p></section>
  );
}
