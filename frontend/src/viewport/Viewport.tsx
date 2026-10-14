import { useCallback, useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import type { ModelPayload } from "../api/types";
import { staleGeometry } from "../state/format";
import { type Animation, frameIndex, framePoses, readout } from "./animation";
import { baseEmissive, baseOpacity, materialFor, rememberEmissive } from "./materials";
import {
  type DisplayMode, type SectionAxis, type StandardView, VIEWS, edgesOf, featureEdges, framing,
  measure, sectionPlane,
} from "./tools";

interface Props {
  model: ModelPayload | null;
  selected: string | null;
  highlighted: string[];
  xray: boolean;
  animation: Animation | null;
  onStop: () => void;
  onSelect: (partId: string | null) => void;
}

interface Scene {
  renderer: THREE.WebGLRenderer;
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera | THREE.OrthographicCamera;
  perspective: THREE.PerspectiveCamera;
  orthographic: THREE.OrthographicCamera;
  controls: OrbitControls;
  root: THREE.Group;
  geometries: Map<string, THREE.BufferGeometry>;
  meshes: Map<string, THREE.Mesh>;
  framed: boolean;
}

interface Measured { a: THREE.Vector3; b: THREE.Vector3 | null }

/** Geometry already held by the viewport, so the backend can skip sending it. */
export const geometryCache = new Map<string, THREE.BufferGeometry>();
const edgeCache = new WeakMap<THREE.BufferGeometry, THREE.EdgesGeometry>();
const FOV = 35;

function toGeometry(vertices: number[], indices: number[]): THREE.BufferGeometry {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
  g.setIndex(indices);
  g.computeVertexNormals();
  g.computeBoundingSphere();
  return g;
}

function modelBox(root: THREE.Group, meshes: Map<string, THREE.Mesh>): THREE.Box3 {
  const box = new THREE.Box3();
  for (const m of meshes.values()) if (m.visible) box.expandByObject(m);
  return box.isEmpty() ? new THREE.Box3().setFromObject(root) : box;
}

function setOrthoFrustum(cam: THREE.OrthographicCamera, half: number, aspect: number) {
  cam.top = half;
  cam.bottom = -half;
  cam.left = -half * aspect;
  cam.right = half * aspect;
  cam.zoom = 1;
  cam.updateProjectionMatrix();
}

export function Viewport({ model, selected, highlighted, xray, animation, onStop, onSelect }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const ctx = useRef<Scene | null>(null);
  const label = useRef<HTMLDivElement>(null);
  const anim = useRef<{ data: Animation; start: number } | null>(null);
  const restore = useRef(false);
  const markers = useRef<THREE.Group | null>(null);
  const [display, setDisplay] = useState<DisplayMode>("shaded");
  const [ortho, setOrtho] = useState(false);
  const [section, setSection] = useState<{ axis: SectionAxis; share: number }>({ axis: "off", share: 0.5 });
  const [measuring, setMeasuring] = useState(false);
  const [measured, setMeasured] = useState<Measured | null>(null);
  const [hidden, setHidden] = useState<Set<string>>(new Set());
  const measuringRef = useRef(measuring);
  measuringRef.current = measuring;

  useEffect(() => {
    anim.current = animation ? { data: animation, start: performance.now() } : null;
    if (!animation) restore.current = true;
  }, [animation]);
  const onSelectRef = useRef(onSelect);
  onSelectRef.current = onSelect;

  // Set up the renderer once.
  useEffect(() => {
    const el = host.current!;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0); // the CSS gradient background shows through
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    // A neutral studio environment for reflections on paint, glass and metal.
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.35;
    renderer.toneMappingExposure = 0.9;
    pmrem.dispose();
    const perspective = new THREE.PerspectiveCamera(FOV, 1, 10, 200000);
    const orthographic = new THREE.OrthographicCamera(-1, 1, 1, -1, -200000, 200000);
    for (const cam of [perspective, orthographic]) cam.up.set(0, 0, 1); // ISO 8855: Z up
    perspective.position.set(4500, -6500, 3200);
    const controls = new OrbitControls(perspective, renderer.domElement);
    controls.enableDamping = true;

    scene.add(new THREE.HemisphereLight(0xdde6f0, 0x2a2a2a, 0.9));
    const sun = new THREE.DirectionalLight(0xffffff, 2.0);
    sun.position.set(3000, -4000, 6000);
    scene.add(sun);

    const grid = new THREE.GridHelper(12000, 24, 0x3a434d, 0x2a3138);
    grid.rotation.x = Math.PI / 2; // into the XY ground plane
    scene.add(grid);

    const root = new THREE.Group();
    scene.add(root);
    const marks = new THREE.Group();
    scene.add(marks);
    markers.current = marks;
    ctx.current = { renderer, scene, camera: perspective, perspective, orthographic, controls, root,
      geometries: geometryCache, meshes: new Map(), framed: false };
    if (import.meta.env.DEV) (window as unknown as { __autevra: unknown }).__autevra = ctx.current;

    // Axis triad in the lower-left corner (X red forward, Y green left, Z blue up).
    const triad = new THREE.Scene();
    const triadAxes = new THREE.AxesHelper(1);
    (triadAxes.material as THREE.Material).toneMapped = false; // keep pure red, green, blue
    triad.add(triadAxes);
    const triadCamera = new THREE.OrthographicCamera(-1.3, 1.3, 1.3, -1.3, -10, 10);

    const resize = () => {
      const { clientWidth: w, clientHeight: h } = el;
      renderer.setSize(w, h);
      perspective.aspect = w / Math.max(h, 1);
      perspective.updateProjectionMatrix();
      setOrthoFrustum(orthographic, orthographic.top || 1, perspective.aspect);
    };
    const observer = new ResizeObserver(resize);
    observer.observe(el);
    resize();

    const raycaster = new THREE.Raycaster();
    let downAt = { x: 0, y: 0 };
    const onDown = (e: PointerEvent) => (downAt = { x: e.clientX, y: e.clientY });
    const onUp = (e: PointerEvent) => {
      if (Math.hypot(e.clientX - downAt.x, e.clientY - downAt.y) > 4) return; // a drag
      const rect = renderer.domElement.getBoundingClientRect();
      const ndc = new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1);
      raycaster.setFromCamera(ndc, ctx.current!.camera);
      const planes = renderer.clippingPlanes;
      const hit = raycaster.intersectObjects(root.children, false).find((h) => h.object.visible
        && planes.every((p) => p.distanceToPoint(h.point) >= 0)); // not in the cut-away part
      if (measuringRef.current) {
        if (hit) setMeasured((m) => (!m || m.b ? { a: hit.point.clone(), b: null } : { a: m.a, b: hit.point.clone() }));
        return;
      }
      onSelectRef.current(hit ? (hit.object.userData.partId as string) : null);
    };
    renderer.domElement.addEventListener("pointerdown", onDown);
    renderer.domElement.addEventListener("pointerup", onUp);

    let frame = 0;
    const meshes = () => ctx.current?.meshes ?? new Map<string, THREE.Mesh>();
    const base = () => new Map([...meshes()].map(([id, m]) => [id, m.userData.base as THREE.Matrix4]));
    const damperLength = (id: string) => {
      const g = meshes().get(id)?.geometry;
      if (!g) return 0;
      if (!g.boundingBox) g.computeBoundingBox();
      return g.boundingBox!.max.z - 18; // upper eye centre (eye radius 18 mm)
    };
    const loop = () => {
      frame = requestAnimationFrame(loop);
      const c = ctx.current;
      if (!c) return;
      const a = anim.current;
      if (a) {
        const i = frameIndex(a.data.t, (performance.now() - a.start) / 1000);
        for (const [id, m] of framePoses(a.data, i, base(), damperLength)) {
          const mesh = meshes().get(id);
          if (mesh) { mesh.matrix.copy(m); mesh.matrixWorldNeedsUpdate = true; }
        }
        if (label.current) label.current.textContent = readout(a.data, i);
      } else if (restore.current) {
        for (const mesh of meshes().values()) {
          mesh.matrix.copy(mesh.userData.base as THREE.Matrix4);
          mesh.matrixWorldNeedsUpdate = true;
        }
        restore.current = false;
      }
      controls.update();
      const { clientWidth: w, clientHeight: h } = el;
      renderer.setViewport(0, 0, w, h);
      renderer.render(scene, c.camera);
      // Triad: the view's orientation, drawn on top in a 90 px corner, never clipped.
      const size = 90;
      triadCamera.position.set(0, 0, 3).applyQuaternion(c.camera.quaternion);
      triadCamera.quaternion.copy(c.camera.quaternion);
      const clipping = renderer.clippingPlanes;
      renderer.clippingPlanes = [];
      renderer.setScissorTest(true);
      renderer.setScissor(8, 8, size, size);
      renderer.setViewport(8, 8, size, size);
      renderer.clearDepth();
      renderer.render(triad, triadCamera);
      renderer.setScissorTest(false);
      renderer.clippingPlanes = clipping;
    };
    loop();

    return () => {
      cancelAnimationFrame(frame);
      observer.disconnect();
      controls.dispose();
      renderer.dispose();
      el.removeChild(renderer.domElement);
      ctx.current = null;
    };
  }, []);

  // Sync meshes with the model: reuse cached geometry, update transforms.
  useEffect(() => {
    const c = ctx.current;
    if (!c || !model) return;
    for (const [key, data] of Object.entries(model.geometries)) {
      c.geometries.get(key)?.dispose();
      c.geometries.delete(key); // re-insert so the LRU order stays correct
      c.geometries.set(key, toGeometry(data.vertices, data.indices));
    }
    for (const part of model.parts) {
      const g = c.geometries.get(part.geometry);
      if (g) { c.geometries.delete(part.geometry); c.geometries.set(part.geometry, g); }
    }
    const ids = new Set(model.parts.map((p) => p.id));
    for (const [id, mesh] of c.meshes) {
      if (!ids.has(id)) {
        c.root.remove(mesh);
        (mesh.material as THREE.Material).dispose();
        c.meshes.delete(id);
      }
    }
    for (const part of model.parts) {
      const geometry = c.geometries.get(part.geometry);
      if (!geometry) continue;
      let mesh = c.meshes.get(part.id);
      if (!mesh) {
        const material = materialFor(part.finish, part.color);
        rememberEmissive(material);
        mesh = new THREE.Mesh(geometry, material);
        mesh.matrixAutoUpdate = false;
        mesh.userData.partId = part.id;
        c.meshes.set(part.id, mesh);
        c.root.add(mesh);
      }
      const look = `${part.finish}|${part.color.join(",")}`;
      if (mesh.userData.look !== undefined && mesh.userData.look !== look) {
        (mesh.material as THREE.Material).dispose(); // repainted: same geometry, new material
        const material = materialFor(part.finish, part.color);
        rememberEmissive(material);
        mesh.material = material;
      }
      mesh.userData.look = look;
      if (mesh.geometry !== geometry) { // rebuilt: its edge outline is stale
        for (const child of [...mesh.children]) if (child.userData.edges) mesh.remove(child);
      }
      mesh.geometry = geometry;
      mesh.userData.category = part.category;
      const m = part.matrix;
      mesh.matrix.set(...(m.flat() as Parameters<THREE.Matrix4["set"]>));
      mesh.userData.base = mesh.matrix.clone();
      mesh.matrixWorldNeedsUpdate = true;
    }
    for (const key of staleGeometry(c.geometries.keys(), model.parts)) {
      c.geometries.get(key)!.dispose();
      c.geometries.delete(key);
    }
    if (!c.framed) {
      const box = new THREE.Box3().setFromObject(c.root);
      const centre = box.getCenter(new THREE.Vector3());
      c.controls.target.copy(centre);
      c.camera.position.set(centre.x + 4200, centre.y - 6000, centre.z + 3000);
      c.framed = true;
    }
  }, [model]);

  // Selection, change highlight, x-ray body, display mode and visibility.
  useEffect(() => {
    const c = ctx.current;
    if (!c) return;
    for (const [id, mesh] of c.meshes) {
      const mat = mesh.material as THREE.MeshStandardMaterial;
      const isBody = mesh.userData.category === "body";
      const own = baseOpacity(mat);
      const opacity = xray && isBody ? Math.min(0.22, own) : own;
      const transparent = opacity < 1;
      const side = section.axis === "off" ? THREE.FrontSide : THREE.DoubleSide; // see inside a cut
      if (mat.transparent !== transparent || mat.side !== side) mat.needsUpdate = true;
      mat.transparent = transparent;
      mat.opacity = opacity;
      mat.depthWrite = !transparent;
      mat.side = side;
      mat.visible = display !== "wireframe";
      if (id === selected) mat.emissive.set(0x3d6fb6);
      else if (highlighted.includes(id)) mat.emissive.set(0x7a5a12);
      else mat.emissive.copy(baseEmissive(mat));
      mesh.visible = !hidden.has(id);

      let edges = mesh.children.find((ch) => ch.userData.edges) as THREE.LineSegments | undefined;
      if (display !== "shaded" && !edges) {
        let g = edgeCache.get(mesh.geometry);
        if (!g) { g = edgesOf(mesh.geometry); edgeCache.set(mesh.geometry, g); }
        edges = featureEdges(g);
        mesh.add(edges);
      }
      if (edges) {
        edges.visible = display !== "shaded";
        (edges.material as THREE.LineBasicMaterial).color.set(
          display === "wireframe" ? (id === selected ? 0x7fb2ff : 0xc9d4e0) : 0x0b0e12);
      }
    }
  }, [model, selected, highlighted, xray, display, hidden, section.axis]);

  // Section plane.
  useEffect(() => {
    const c = ctx.current;
    if (!c) return;
    c.renderer.clippingPlanes = section.axis === "off"
      ? [] : [sectionPlane(modelBox(c.root, c.meshes), section.axis, section.share)];
  }, [section, model]);

  // Measurement markers.
  useEffect(() => {
    const marks = markers.current;
    if (!marks) return;
    for (const child of [...marks.children]) marks.remove(child);
    if (!measuring || !measured) return;
    const dot = (p: THREE.Vector3) => {
      const s = new THREE.Mesh(new THREE.SphereGeometry(18, 16, 12),
        new THREE.MeshBasicMaterial({ color: 0xffc94a, depthTest: false }));
      s.position.copy(p);
      s.renderOrder = 10;
      marks.add(s);
    };
    dot(measured.a);
    if (measured.b) {
      dot(measured.b);
      const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints([measured.a, measured.b]),
        new THREE.LineBasicMaterial({ color: 0xffc94a, depthTest: false }));
      line.renderOrder = 10;
      marks.add(line);
    }
  }, [measured, measuring]);

  const viewFrom = useCallback((view: StandardView) => {
    const c = ctx.current;
    if (!c) return;
    const box = modelBox(c.root, c.meshes);
    if (box.isEmpty()) return;
    const f = framing(box, view, FOV, c.perspective.aspect);
    for (const cam of [c.perspective, c.orthographic]) {
      cam.up.copy(f.up);
      cam.position.copy(f.position);
      cam.lookAt(f.target);
    }
    setOrthoFrustum(c.orthographic, f.radius * 1.1, c.perspective.aspect);
    c.controls.target.copy(f.target);
    c.controls.update();
  }, []);

  const toggleOrtho = () => {
    const c = ctx.current;
    if (!c) return;
    const next = !ortho;
    const from = c.camera, to = next ? c.orthographic : c.perspective;
    to.position.copy(from.position);
    to.quaternion.copy(from.quaternion);
    to.up.copy(from.up);
    if (next) {
      const half = from.position.distanceTo(c.controls.target) * Math.tan(THREE.MathUtils.degToRad(FOV / 2));
      setOrthoFrustum(c.orthographic, half, c.perspective.aspect);
    }
    c.camera = to;
    c.controls.object = to;
    c.controls.update();
    setOrtho(next);
  };

  const ids = model?.parts.map((p) => p.id) ?? [];
  const result = measured?.b ? measure(measured.a, measured.b) : null;
  const mm = (v: number) => `${v.toFixed(1)} mm`;

  return (
    <>
      <div className="viewport" ref={host} />
      <div className="cad-toolbar" role="toolbar" aria-label="View tools">
        <div className="seg" aria-label="Display mode">
          {(["shaded", "edges", "wireframe"] as DisplayMode[]).map((d) => (
            <button key={d} className={display === d ? "on" : ""} onClick={() => setDisplay(d)}
              title={{ shaded: "Shading", edges: "Shading with edges", wireframe: "Wireframe (edges only)" }[d]}>
              {{ shaded: "Shaded", edges: "Edges", wireframe: "Wire" }[d]}
            </button>
          ))}
        </div>
        <div className="seg" aria-label="Standard views">
          {(Object.keys(VIEWS) as StandardView[]).map((v) => (
            <button key={v} onClick={() => viewFrom(v)} title={`${VIEWS[v].label} view`}>
              {v === "iso" ? "Iso" : VIEWS[v].label}
            </button>
          ))}
          <button className={ortho ? "on" : ""} onClick={toggleOrtho} title="Orthographic or perspective projection">
            {ortho ? "Ortho" : "Persp"}
          </button>
        </div>
        <div className="seg" aria-label="Section">
          <select value={section.axis} aria-label="Section plane"
            onChange={(e) => setSection({ ...section, axis: e.target.value as SectionAxis })}>
            <option value="off">No section</option>
            <option value="x">Section X (along)</option>
            <option value="y">Section Y (across)</option>
            <option value="z">Section Z (height)</option>
          </select>
          {section.axis !== "off" && (
            <input type="range" min={0} max={1} step={0.01} value={section.share} aria-label="Section position"
              onChange={(e) => setSection({ ...section, share: Number(e.target.value) })} />
          )}
        </div>
        <div className="seg" aria-label="Measure and visibility">
          <button className={measuring ? "on" : ""} title="Measure the distance between two picked points"
            onClick={() => { setMeasuring(!measuring); setMeasured(null); }}>Measure</button>
          <button disabled={!selected} title="Hide the selected component"
            onClick={() => selected && setHidden(new Set([...hidden, selected]))}>Hide</button>
          <button disabled={!selected} title="Show only the selected component"
            onClick={() => selected && setHidden(new Set(ids.filter((i) => i !== selected)))}>Isolate</button>
          <button disabled={hidden.size === 0} onClick={() => setHidden(new Set())}>Show all</button>
        </div>
      </div>
      {measuring && (
        <div className="cad-readout">
          {!measured ? "Pick the first point on the model"
            : !result ? "Pick the second point"
            : <>Distance <strong>{mm(result.distance)}</strong> · ΔX {mm(result.dx)} · ΔY {mm(result.dy)} · ΔZ {mm(result.dz)}</>}
        </div>
      )}
      <div className="cad-triad-legend">X fwd · Y left · Z up</div>
      {animation && (
        <div className="playback">
          <span ref={label}>{animation.label}</span>
          <button onClick={onStop}>Stop</button>
        </div>
      )}
    </>
  );
}
