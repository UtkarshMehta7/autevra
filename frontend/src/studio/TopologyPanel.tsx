import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { api } from "../api/client";
import type { TopologyRequest, TopologyResult } from "../api/types";

/** Topology optimisation by SIMP: the density field as it evolves (2D grid or 3D voxels),
 * the compliance history, and the equations and numbers behind each step (backend
 * fea/simp.py). */
export function TopologyPanel() {
  const [cases, setCases] = useState<Record<string, string>>({});
  const [req, setReq] = useState<TopologyRequest>({
    case: "mbb", nx: 60, ny: 20, nz: 0, volfrac: 0.5, penal: 3, rmin: 1.5, max_iter: 120,
  });
  const [result, setResult] = useState<TopologyResult | null>(null);
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [threshold, setThreshold] = useState(0.5);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => { api.topologyCases().then((c) => setCases(c.cases)).catch(() => setCases({})); }, []);
  useEffect(() => {
    if (!playing || !result) return;
    const id = window.setInterval(() => setFrame((f) => {
      if (f >= result.snapshots.length - 1) { setPlaying(false); return f; }
      return f + 1;
    }), 120);
    return () => window.clearInterval(id);
  }, [playing, result]);

  const run = async () => {
    setBusy(true);
    setError(null);
    try {
      const out = await api.topology(req);
      setResult(out);
      setFrame(0);
      setPlaying(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  const field = result ? result.snapshots[Math.min(frame, result.snapshots.length - 1)] : null;
  const iter = result ? result.snapshot_iters[Math.min(frame, result.snapshot_iters.length - 1)] : 0;
  const is3d = (result?.shape.length ?? (req.nz > 0 ? 3 : 2)) === 3;
  const num = (key: keyof TopologyRequest, label: string, min: number, max: number, step: number, width = 52) => (
    <label>{label} <input type="number" min={min} max={max} step={step} value={req[key] as number} style={{ width }}
      onChange={(e) => setReq({ ...req, [key]: Number(e.target.value) })} /></label>
  );
  const s = result?.stats;
  const h = result?.history[Math.max(0, Math.min(iter, result.history.length) - 1)];

  return (
    <div className="bench wide surfaces-lab structures">
      <div className="lab-view">
        {result && field && (is3d
          ? <VoxelView shape={result.shape} density={field} threshold={threshold} />
          : <DensityCanvas shape={result.shape} density={field} />)}
        {!result && <div className="lab-busy">Pick a load case and run the optimiser</div>}
        {busy && <div className="lab-busy">Optimising: solving K(x) u = F each iteration…</div>}
        {result && (
          <div className="legend">
            <label>iteration {iter} of {s?.iterations}
              <input type="range" min={0} max={result.snapshots.length - 1} value={frame}
                onChange={(e) => { setPlaying(false); setFrame(Number(e.target.value)); }} />
            </label>
            <div className="row">
              <button onClick={() => { if (frame >= result.snapshots.length - 1) setFrame(0); setPlaying(!playing); }}>
                {playing ? "Pause" : "Play"}</button>
              {is3d && <label>show x ≥ {threshold.toFixed(2)}
                <input type="range" min={0.05} max={0.95} step={0.05} value={threshold}
                  onChange={(e) => setThreshold(Number(e.target.value))} /></label>}
            </div>
          </div>
        )}
      </div>
      <div className="lab-side">
        <div className="row">
          <select value={req.case} onChange={(e) => setReq({ ...req, case: e.target.value as TopologyRequest["case"] })}>
            {Object.entries(cases).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
          <label><input type="checkbox" checked={req.nz > 0} onChange={(e) => setReq(e.target.checked
            ? { ...req, nx: 24, ny: 8, nz: 6, volfrac: 0.3, max_iter: 50 }
            : { ...req, nx: 60, ny: 20, nz: 0, volfrac: 0.5, max_iter: 120 })} /> 3D voxels</label>
        </div>
        <div className="row">
          {num("nx", "nx", 4, 200, 2)}{num("ny", req.nz > 0 ? "ny" : "ny (height)", 2, 100, 2)}
          {req.nz > 0 && num("nz", "nz (height)", 2, 40, 1)}
        </div>
        <div className="row">
          {num("volfrac", "volume f", 0.06, 0.94, 0.05)}{num("penal", "penalty p", 1, 5, 0.5)}
          {num("rmin", "filter r", 1, 6, 0.25)}{num("max_iter", "max iterations", 1, 300, 10, 60)}
        </div>
        <div className="row">
          <button className="primary" disabled={busy} onClick={run}>{busy ? "Optimising…" : "Optimise"}</button>
          {error && <span className="error">{error}</span>}
        </div>
        {result && s && h && (
          <>
            <div className="muted">{result.description}</div>
            <div className="math">
              {result.equations.map((e) => <div key={e}>{e}</div>)}
            </div>
            <div className="math">
              <div>Domain {result.shape.join(" × ")} = {s.elements.toLocaleString()} elements, {s.dofs.toLocaleString()} DOFs ({s.free_dofs.toLocaleString()} free); k₀ has {s.k_nnz_per_element} entries</div>
              <div>Iteration {h.iter}: c = {h.compliance.toPrecision(5)}, volume {(h.volume * 100).toFixed(1)} %, max |Δx| {h.change.toFixed(3)}, grey (0.1 &lt; x &lt; 0.9) {(h.grey * 100).toFixed(1)} %, λ = {h.lambda.toExponential(2)}</div>
              <div className={s.converged ? "good-text" : ""}>
                {s.converged ? "Converged" : "Stopped"} after {s.iterations} iterations: c {s.initial_compliance.toPrecision(4)} → {s.final_compliance.toPrecision(4)} ({((1 - s.final_compliance / s.initial_compliance) * 100).toFixed(0)} % stiffer for the same material)</div>
              <div>Filter: {s.filter_neighbours.toFixed(1)} neighbours per element · solver {s.solver} · {(s.time_solve * 1000).toFixed(0)} ms solving of {(s.time_total * 1000).toFixed(0)} ms</div>
            </div>
            <History result={result} at={h.iter} />
          </>
        )}
      </div>
    </div>
  );
}

/** The density field of a 2D domain (black = solid, white = void), y up. */
function DensityCanvas({ shape, density }: { shape: number[]; density: number[] }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const [nx, ny] = shape;
  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    canvas.width = nx;
    canvas.height = ny;
    const ctx = canvas.getContext("2d")!;
    const img = ctx.createImageData(nx, ny);
    for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const v = Math.round(255 * (1 - Math.max(0, Math.min(1, density[j * nx + i]))));
      const o = ((ny - 1 - j) * nx + i) * 4;
      img.data[o] = v; img.data[o + 1] = v; img.data[o + 2] = v; img.data[o + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
  }, [density, nx, ny]);
  return <canvas ref={ref} className="density-canvas" style={{ aspectRatio: `${nx} / ${ny}` }} />;
}

/** Voxels at or above the density threshold, shaded by density. */
function VoxelView({ shape, density, threshold }: { shape: number[]; density: number[]; threshold: number }) {
  const host = useRef<HTMLDivElement>(null);
  const ctx = useRef<{ renderer: THREE.WebGLRenderer; scene: THREE.Scene; camera: THREE.PerspectiveCamera;
    controls: OrbitControls; mesh: THREE.InstancedMesh | null; framed: string } | null>(null);

  useEffect(() => {
    const el = host.current!;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    el.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    scene.add(new THREE.HemisphereLight(0xffffff, 0x303030, 1.4));
    const sun = new THREE.DirectionalLight(0xffffff, 1.6);
    sun.position.set(-30, -50, 80);
    scene.add(sun);
    const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 1e4);
    camera.up.set(0, 0, 1);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    ctx.current = { renderer, scene, camera, controls, mesh: null, framed: "" };
    const resize = () => {
      renderer.setSize(el.clientWidth, el.clientHeight);
      camera.aspect = el.clientWidth / Math.max(el.clientHeight, 1);
      camera.updateProjectionMatrix();
    };
    const ro = new ResizeObserver(resize);
    ro.observe(el);
    resize();
    let id = 0;
    const loop = () => { id = requestAnimationFrame(loop); controls.update(); renderer.render(scene, camera); };
    loop();
    return () => { cancelAnimationFrame(id); ro.disconnect(); controls.dispose(); renderer.dispose(); el.removeChild(renderer.domElement); ctx.current = null; };
  }, []);

  const cells = useMemo(() => {
    const [nx, ny, nz] = shape;
    const out: [number, number, number, number][] = [];
    for (let k = 0; k < nz; k++) for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
      const v = density[(k * ny + j) * nx + i];
      if (v >= threshold) out.push([i, j, k, v]);
    }
    return out;
  }, [shape, density, threshold]);

  useEffect(() => {
    const c = ctx.current;
    if (!c) return;
    if (c.mesh) { c.scene.remove(c.mesh); c.mesh.geometry.dispose(); (c.mesh.material as THREE.Material).dispose(); }
    const mesh = new THREE.InstancedMesh(new THREE.BoxGeometry(0.96, 0.96, 0.96),
      new THREE.MeshStandardMaterial({ roughness: 0.55, metalness: 0.1 }), Math.max(cells.length, 1));
    const m = new THREE.Matrix4(), col = new THREE.Color();
    cells.forEach(([i, j, k, v], n) => {
      m.makeTranslation(i + 0.5, j + 0.5, k + 0.5);
      mesh.setMatrixAt(n, m);
      mesh.setColorAt(n, col.setRGB(0.25 + 0.5 * (1 - v), 0.45 + 0.35 * (1 - v), 0.75));
    });
    mesh.count = cells.length;
    c.scene.add(mesh);
    c.mesh = mesh;
    const key = shape.join("x");
    if (c.framed !== key) {
      const [nx, ny, nz] = shape;
      const centre = new THREE.Vector3(nx / 2, ny / 2, nz / 2);
      const r = Math.hypot(nx, ny, nz) / 2;
      c.controls.target.copy(centre);
      c.camera.position.copy(centre).add(new THREE.Vector3(0.6, -1.6, 0.9).normalize().multiplyScalar(r * 3.2));
      c.framed = key;
    }
  }, [cells, shape]);

  return <div className="surface-view" ref={host} />;
}

function History({ result, at }: { result: TopologyResult; at: number }) {
  const W = 320, H = 90, L = 34;
  const c = result.history.map((h) => h.compliance);
  const lo = Math.min(...c), hi = Math.max(...c);
  const x = (i: number) => L + (i / Math.max(c.length - 1, 1)) * (W - L - 6);
  const y = (v: number) => 8 + (1 - (v - lo) / Math.max(hi - lo, 1e-12)) * (H - 22);
  const g = (v: number) => 8 + (1 - v) * (H - 22);
  return (
    <svg className="chart convergence" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Compliance per iteration">
      <text x={L} y={7} className="chart-title">compliance c (blue) and grey fraction (amber) per iteration</text>
      <line x1={L} x2={W - 4} y1={H - 14} y2={H - 14} className="grid" />
      <text x={L - 3} y={y(hi) + 3} textAnchor="end" className="tick">{hi.toPrecision(3)}</text>
      <text x={L - 3} y={y(lo) + 3} textAnchor="end" className="tick">{lo.toPrecision(3)}</text>
      <path className="series" d={c.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join("")} />
      <path fill="none" stroke="#ffc94a" strokeWidth={1} d={result.history.map((h, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${g(h.grey).toFixed(1)}`).join("")} />
      <line x1={x(at - 1)} x2={x(at - 1)} y1={6} y2={H - 14} stroke="#fff" strokeOpacity={0.4} />
      <text x={W - 4} y={H - 3} textAnchor="end" className="tick">{c.length} iterations</text>
    </svg>
  );
}
