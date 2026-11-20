import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import type { FeaMesh, FeaResult } from "../api/types";

export type FeaField = "magnitude" | "von_mises" | "principal_1" | "strain_eq";

/** A perceptual rainbow (blue - cyan - green - yellow - red) for a value in [0, 1]. */
export function rainbow(t: number): [number, number, number] {
  const x = Math.max(0, Math.min(1, t));
  const stops: [number, [number, number, number]][] = [
    [0, [0.19, 0.27, 0.78]], [0.25, [0.1, 0.65, 0.92]], [0.5, [0.25, 0.8, 0.35]],
    [0.75, [0.97, 0.82, 0.18]], [1, [0.86, 0.17, 0.12]],
  ];
  for (let i = 1; i < stops.length; i++) {
    const [t1, c1] = stops[i];
    const [t0, c0] = stops[i - 1];
    if (x <= t1) {
      const f = (x - t0) / (t1 - t0);
      return [c0[0] + f * (c1[0] - c0[0]), c0[1] + f * (c1[1] - c0[1]), c0[2] + f * (c1[2] - c0[2])];
    }
  }
  return stops[stops.length - 1][1];
}

interface Props {
  result: FeaResult | null;
  preview?: FeaMesh | null; // a mesh to pick faces on before solving
  field: FeaField;
  scale: number; // deformation magnification
  edges: boolean;
  roles?: Record<number, "support" | "load">; // B-rep face id -> role, shown on the preview
  onPick?: (face: number) => void;
}

const ROLE_COLOURS = { support: [0.31, 0.53, 0.84], load: [1.0, 0.6, 0.24], none: [0.62, 0.65, 0.7] } as const;

/** Results on the deformed surface of the mesh, with the undeformed outline, supports
 * (blue) and loaded nodes (orange). */
export function FeaView({ result, preview, field, scale, edges, roles, onPick }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const pick = useRef<((triangle: number) => void) | null>(null);
  const ctx = useRef<{ renderer: THREE.WebGLRenderer; scene: THREE.Scene; camera: THREE.PerspectiveCamera;
    controls: OrbitControls; content: THREE.Group; framed: string } | null>(null);

  useEffect(() => {
    const el = host.current!;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    el.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    scene.add(new THREE.HemisphereLight(0xffffff, 0x404040, 1.6));
    const sun = new THREE.DirectionalLight(0xffffff, 1.2);
    sun.position.set(300, -400, 600);
    scene.add(sun);
    const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 1e6);
    camera.up.set(0, 0, 1);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    const content = new THREE.Group();
    scene.add(content);
    ctx.current = { renderer, scene, camera, controls, content, framed: "" };
    // a click (not a drag) picks the B-rep face under the cursor
    let down: [number, number] | null = null;
    const ray = new THREE.Raycaster();
    renderer.domElement.addEventListener("pointerdown", (e) => { down = [e.clientX, e.clientY]; });
    renderer.domElement.addEventListener("pointerup", (e) => {
      if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 4) return;
      const r = renderer.domElement.getBoundingClientRect();
      ray.setFromCamera(new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1), camera);
      const surface = content.children.find((o) => o.userData.pickable);
      const hit = surface ? ray.intersectObject(surface)[0] : undefined;
      if (hit?.faceIndex != null) pick.current?.(hit.faceIndex);
    });
    const resize = () => {
      const { clientWidth: w, clientHeight: h } = el;
      renderer.setSize(w, h);
      camera.aspect = w / Math.max(h, 1);
      camera.updateProjectionMatrix();
    };
    const ro = new ResizeObserver(resize);
    ro.observe(el);
    resize();
    let frame = 0;
    const loop = () => { frame = requestAnimationFrame(loop); controls.update(); renderer.render(scene, camera); };
    loop();
    return () => { cancelAnimationFrame(frame); ro.disconnect(); controls.dispose(); renderer.dispose(); el.removeChild(renderer.domElement); ctx.current = null; };
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
    const mesh = result?.mesh ?? preview;
    pick.current = null;
    if (!mesh) return;
    const { nodes, boundary } = mesh;
    pick.current = (t) => { const face = mesh.boundary_face[t]; if (face != null) onPick?.(face); };
    const disp = result?.fields.displacement;
    const values = result?.fields[field];
    let lo = Infinity, hi = -Infinity;
    for (const v of values ?? []) { if (v < lo) lo = v; if (v > hi) hi = v; }
    const span = hi - lo || 1;
    const pos: number[] = [], col: number[] = [], rest: number[] = [];
    boundary.forEach((tri, t) => {
      const role = roles?.[mesh.boundary_face[t]] ?? "none";
      for (const n of tri) {
        const p = nodes[n], u = disp?.[n] ?? [0, 0, 0];
        const s = disp ? scale : 0;
        pos.push(p[0] + s * u[0], p[1] + s * u[1], p[2] + s * u[2]);
        rest.push(...p);
        col.push(...(values ? rainbow((values[n] - lo) / span) : ROLE_COLOURS[role]));
      }
    });
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
    g.computeVertexNormals();
    const surface = new THREE.Mesh(g, new THREE.MeshLambertMaterial({ vertexColors: true, side: THREE.DoubleSide }));
    surface.userData.pickable = true;
    c.content.add(surface);
    if (edges) {
      const eg = new THREE.EdgesGeometry(g, 1);
      c.content.add(new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: 0x111418, transparent: true, opacity: 0.35 })));
    }
    if (result && scale > 0) {
      const rg = new THREE.BufferGeometry();
      rg.setAttribute("position", new THREE.Float32BufferAttribute(rest, 3));
      c.content.add(new THREE.LineSegments(new THREE.EdgesGeometry(rg, 30),
        new THREE.LineBasicMaterial({ color: 0x9aa6b2, transparent: true, opacity: 0.45 })));
    }
    const markers = (ids: number[], color: number) => {
      const pts: number[] = [];
      for (const n of ids) pts.push(...nodes[n]);
      const mg = new THREE.BufferGeometry();
      mg.setAttribute("position", new THREE.Float32BufferAttribute(pts, 3));
      c.content.add(new THREE.Points(mg, new THREE.PointsMaterial({ color, size: 5, sizeAttenuation: false, depthTest: false })));
    };
    if (result) {
      markers(result.supports, 0x4f86d6);
      markers(Object.values(result.loaded).flat(), 0xff9a3c);
    }
    const key = `${nodes.length}:${nodes[0]?.join(",")}`;
    if (c.framed !== key) {
      const box = new THREE.Box3().setFromBufferAttribute(new THREE.Float32BufferAttribute(rest, 3));
      const centre = box.getCenter(new THREE.Vector3());
      const r = box.getBoundingSphere(new THREE.Sphere()).radius;
      const half = THREE.MathUtils.degToRad(c.camera.fov / 2);
      const fit = r / Math.sin(Math.min(half, Math.atan(Math.tan(half) * c.camera.aspect)));
      c.controls.target.copy(centre);
      c.camera.position.copy(centre).add(new THREE.Vector3(0.9, -1.6, 0.9).normalize().multiplyScalar(fit * 1.05));
      c.camera.near = r / 100;
      c.camera.far = r * 100;
      c.camera.updateProjectionMatrix();
      c.framed = key;
    }
  }, [result, preview, field, scale, edges, roles, onPick]);

  return <div className="surface-view" ref={host} />;
}
