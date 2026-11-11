import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import type { NurbsEvaluation } from "../api/types";

export type SurfaceColour = "shaded" | "gaussian" | "mean";

interface Patch {
  evaluation: NurbsEvaluation;
  editable: boolean; // its control points can be picked and dragged
  tint: number;
}

interface Props {
  patches: Patch[];
  colour: SurfaceColour;
  selected: { patch: number; i: number; j: number } | null;
  onSelect: (sel: { patch: number; i: number; j: number } | null) => void;
  onDrag: (sel: { patch: number; i: number; j: number }, to: [number, number, number], done: boolean) => void;
  combs?: { points: [number, number, number][]; tips: [number, number, number][] }[];
  lattice: boolean;
}

/** Diverging colour for a signed value: blue (negative), white (zero), red (positive). */
export function diverging(value: number, range: number): [number, number, number] {
  const t = Math.max(-1, Math.min(1, value / Math.max(range, 1e-12)));
  return t < 0 ? [1 + t * 0.85, 1 + t * 0.55, 1] : [1, 1 - t * 0.6, 1 - t * 0.85];
}

/** A robust colour range: the 95th percentile of |values| (one spike does not wash out the map). */
export function robustRange(values: number[]): number {
  const a = values.map(Math.abs).sort((x, y) => x - y);
  return a.length ? a[Math.min(a.length - 1, Math.floor(a.length * 0.95))] || a[a.length - 1] || 1 : 1;
}

/** 3D view of NURBS patches with their control lattices, curvature colouring, the selected
 * control point's local support, and curvature combs. Pick a lattice point to select it and
 * drag it in the screen plane. */
export function SurfaceView({ patches, colour, selected, onSelect, onDrag, combs, lattice }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const ctx = useRef<{ renderer: THREE.WebGLRenderer; scene: THREE.Scene; camera: THREE.PerspectiveCamera;
    controls: OrbitControls; content: THREE.Group; framed: number } | null>(null);
  const handles = useRef<THREE.Mesh[]>([]);
  const props = useRef({ onSelect, onDrag, selected });
  props.current = { onSelect, onDrag, selected };

  useEffect(() => {
    const el = host.current!;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    el.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.5;
    pmrem.dispose();
    scene.add(new THREE.HemisphereLight(0xdde6f0, 0x2a2a2a, 0.8));
    const sun = new THREE.DirectionalLight(0xffffff, 1.6);
    sun.position.set(300, -400, 600);
    scene.add(sun);
    const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 1e6);
    camera.up.set(0, 0, 1);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    const content = new THREE.Group();
    scene.add(content);
    ctx.current = { renderer, scene, camera, controls, content, framed: 0 };

    const resize = () => {
      const { clientWidth: w, clientHeight: h } = el;
      renderer.setSize(w, h);
      camera.aspect = w / Math.max(h, 1);
      camera.updateProjectionMatrix();
    };
    const ro = new ResizeObserver(resize);
    ro.observe(el);
    resize();

    const ray = new THREE.Raycaster();
    let drag: { sel: { patch: number; i: number; j: number }; plane: THREE.Plane } | null = null;
    const ndc = (e: PointerEvent) => {
      const r = renderer.domElement.getBoundingClientRect();
      return new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    };
    const down = (e: PointerEvent) => {
      ray.setFromCamera(ndc(e), camera);
      const hit = ray.intersectObjects(handles.current, false)[0];
      if (!hit) return;
      const sel = hit.object.userData.sel as { patch: number; i: number; j: number };
      props.current.onSelect(sel);
      const normal = camera.getWorldDirection(new THREE.Vector3());
      drag = { sel, plane: new THREE.Plane().setFromNormalAndCoplanarPoint(normal, hit.object.position) };
      controls.enabled = false;
      renderer.domElement.setPointerCapture(e.pointerId);
    };
    const move = (e: PointerEvent) => {
      if (!drag) return;
      ray.setFromCamera(ndc(e), camera);
      const p = ray.ray.intersectPlane(drag.plane, new THREE.Vector3());
      if (p) props.current.onDrag(drag.sel, [p.x, p.y, p.z], false);
    };
    const up = (e: PointerEvent) => {
      if (!drag) return;
      ray.setFromCamera(ndc(e), camera);
      const p = ray.ray.intersectPlane(drag.plane, new THREE.Vector3());
      if (p) props.current.onDrag(drag.sel, [p.x, p.y, p.z], true);
      drag = null;
      controls.enabled = true;
    };
    renderer.domElement.addEventListener("pointerdown", down);
    renderer.domElement.addEventListener("pointermove", move);
    renderer.domElement.addEventListener("pointerup", up);
    let frame = 0;
    const loop = () => {
      frame = requestAnimationFrame(loop);
      controls.update();
      renderer.render(scene, camera);
    };
    loop();
    return () => {
      cancelAnimationFrame(frame);
      ro.disconnect();
      controls.dispose();
      renderer.dispose();
      el.removeChild(renderer.domElement);
      ctx.current = null;
    };
  }, []);

  useEffect(() => {
    const c = ctx.current;
    if (!c) return;
    for (const child of [...c.content.children]) {
      c.content.remove(child);
      child.traverse((o) => {
        const m = o as THREE.Mesh;
        m.geometry?.dispose();
        (Array.isArray(m.material) ? m.material : [m.material]).forEach((x) => x?.dispose());
      });
    }
    handles.current = [];
    const box = new THREE.Box3();
    patches.forEach((patch, k) => {
      const { grid, surface } = patch.evaluation;
      const g = new THREE.BufferGeometry();
      g.setAttribute("position", new THREE.Float32BufferAttribute(grid.points.flat(), 3));
      g.setAttribute("normal", new THREE.Float32BufferAttribute(grid.normals.flat(), 3));
      g.setIndex(grid.triangles);
      const values = colour === "gaussian" ? grid.gaussian : colour === "mean" ? grid.mean : null;
      const support = selected?.patch === k ? patch.evaluation.support : null;
      const colours: number[] = [];
      const range = values ? robustRange(values) : 1;
      const base = new THREE.Color(patch.tint);
      grid.u.forEach((u) => grid.v.forEach((v, jj) => {
        const idx = colours.length / 3;
        if (values) {
          colours.push(...diverging(values[idx], range));
        } else if (support && u >= support.u[0] && u <= support.u[1] && v >= support.v[0] && v <= support.v[1]) {
          colours.push(1.0, 0.72, 0.25); // where this control point moves the surface
        } else {
          colours.push(base.r, base.g, base.b);
        }
        void jj;
      }));
      g.setAttribute("color", new THREE.Float32BufferAttribute(colours, 3));
      const mesh = new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({
        vertexColors: true, side: THREE.DoubleSide, roughness: 0.35, metalness: 0.05, clearcoat: 0.6 }));
      c.content.add(mesh);
      box.expandByObject(mesh);

      // Isoparametric curves (every 4th sample) for the parametrisation.
      const iso: number[] = [];
      const nu = grid.u.length, nv = grid.v.length;
      const P = (a: number, b: number) => grid.points[a * nv + b];
      for (let a = 0; a < nu; a += 4) for (let b = 1; b < nv; b++) iso.push(...P(a, b - 1), ...P(a, b));
      for (let b = 0; b < nv; b += 4) for (let a = 1; a < nu; a++) iso.push(...P(a - 1, b), ...P(a, b));
      const isoG = new THREE.BufferGeometry();
      isoG.setAttribute("position", new THREE.Float32BufferAttribute(iso, 3));
      c.content.add(new THREE.LineSegments(isoG, new THREE.LineBasicMaterial({ color: 0x223040, transparent: true, opacity: 0.35 })));

      if (lattice) {
        const pts = surface.control;
        const lines: number[] = [];
        for (let i = 0; i < pts.length; i++) {
          for (let j = 0; j < pts[i].length; j++) {
            if (i > 0) lines.push(...pts[i - 1][j], ...pts[i][j]);
            if (j > 0) lines.push(...pts[i][j - 1], ...pts[i][j]);
          }
        }
        const lg = new THREE.BufferGeometry();
        lg.setAttribute("position", new THREE.Float32BufferAttribute(lines, 3));
        c.content.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({
          color: patch.editable ? 0x6fa8ff : 0x7d8796, depthTest: false, transparent: true, opacity: 0.8 })));
        const size = Math.max(box.getSize(new THREE.Vector3()).length() * 0.008, 0.5);
        pts.forEach((row, i) => row.forEach((p, j) => {
          const on = selected?.patch === k && selected.i === i && selected.j === j;
          const w = surface.weights[i][j];
          const s = new THREE.Mesh(new THREE.SphereGeometry(size * (on ? 1.6 : 1) * Math.cbrt(w), 14, 10),
            new THREE.MeshBasicMaterial({ color: on ? 0xffc94a : patch.editable ? 0x9cc3ff : 0xaab3bf, depthTest: false }));
          s.position.set(...p);
          s.renderOrder = 10;
          s.userData.sel = { patch: k, i, j };
          c.content.add(s);
          if (patch.editable) handles.current.push(s);
        }));
      }
    });
    if (combs?.length) {
      const teeth: number[] = [], spine: number[] = [];
      for (const comb of combs) {
        comb.points.forEach((p, i) => {
          teeth.push(...p, ...comb.tips[i]);
          if (i > 0) spine.push(...comb.tips[i - 1], ...comb.tips[i]);
        });
      }
      for (const [arr, col] of [[teeth, 0xd9a441], [spine, 0xffd27a]] as const) {
        const cg = new THREE.BufferGeometry();
        cg.setAttribute("position", new THREE.Float32BufferAttribute(arr, 3));
        c.content.add(new THREE.LineSegments(cg, new THREE.LineBasicMaterial({ color: col, depthTest: false })));
      }
    }
    if (c.framed !== patches.length && !box.isEmpty()) { // frame again when a patch comes or goes
      const centre = box.getCenter(new THREE.Vector3());
      const r = box.getBoundingSphere(new THREE.Sphere()).radius;
      c.controls.target.copy(centre);
      // Fit the bounding sphere in the narrower of the two fields of view.
      const half = THREE.MathUtils.degToRad(c.camera.fov / 2);
      const fit = r / Math.sin(Math.min(half, Math.atan(Math.tan(half) * c.camera.aspect)));
      c.camera.position.copy(centre).add(new THREE.Vector3(1.3, -2.0, 1.5).normalize().multiplyScalar(fit * 1.05));
      c.camera.near = r / 100;
      c.camera.far = r * 100;
      c.camera.updateProjectionMatrix();
      c.framed = patches.length;
    }
  }, [patches, colour, selected, combs, lattice]);

  return <div className="surface-view" ref={host} />;
}
