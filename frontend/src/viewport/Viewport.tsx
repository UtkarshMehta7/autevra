import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import type { ModelPayload } from "../api/types";
import { staleGeometry } from "../state/format";
import { type Animation, frameIndex, framePoses, readout } from "./animation";

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
  camera: THREE.PerspectiveCamera;
  controls: OrbitControls;
  root: THREE.Group;
  geometries: Map<string, THREE.BufferGeometry>;
  meshes: Map<string, THREE.Mesh>;
  framed: boolean;
}

/** Geometry already held by the viewport, so the backend can skip sending it. */
export const geometryCache = new Map<string, THREE.BufferGeometry>();

function toGeometry(vertices: number[], indices: number[]): THREE.BufferGeometry {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
  g.setIndex(indices);
  g.computeVertexNormals();
  g.computeBoundingSphere();
  return g;
}

export function Viewport({ model, selected, highlighted, xray, animation, onStop, onSelect }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const ctx = useRef<Scene | null>(null);
  const label = useRef<HTMLDivElement>(null);
  const anim = useRef<{ data: Animation; start: number } | null>(null);
  const restore = useRef(false);
  useEffect(() => {
    anim.current = animation ? { data: animation, start: performance.now() } : null;
    if (!animation) restore.current = true;
  }, [animation]);
  const onSelectRef = useRef(onSelect);
  onSelectRef.current = onSelect;

  // Set up the renderer once.
  useEffect(() => {
    const el = host.current!;
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1b1f24);
    const camera = new THREE.PerspectiveCamera(35, 1, 10, 200000);
    camera.up.set(0, 0, 1); // ISO 8855: Z up
    camera.position.set(4500, -6500, 3200);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    scene.add(new THREE.HemisphereLight(0xdde6f0, 0x2a2a2a, 1.6));
    const sun = new THREE.DirectionalLight(0xffffff, 2.2);
    sun.position.set(3000, -4000, 6000);
    scene.add(sun);

    const grid = new THREE.GridHelper(12000, 24, 0x3a434d, 0x2a3138);
    grid.rotation.x = Math.PI / 2; // into the XY ground plane
    scene.add(grid);
    const axes = new THREE.AxesHelper(600); // X red forward, Y green left, Z blue up
    scene.add(axes);

    const root = new THREE.Group();
    scene.add(root);
    ctx.current = { renderer, scene, camera, controls, root, geometries: geometryCache,
      meshes: new Map(), framed: false };
    if (import.meta.env.DEV) (window as unknown as { __autevra: unknown }).__autevra = ctx.current;

    const resize = () => {
      const { clientWidth: w, clientHeight: h } = el;
      renderer.setSize(w, h);
      camera.aspect = w / Math.max(h, 1);
      camera.updateProjectionMatrix();
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
      raycaster.setFromCamera(ndc, camera);
      const hit = raycaster.intersectObjects(root.children, false)[0];
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
      renderer.render(scene, camera);
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
        mesh = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
          color: new THREE.Color(...part.color), metalness: 0.2, roughness: 0.6,
        }));
        mesh.matrixAutoUpdate = false;
        mesh.userData.partId = part.id;
        c.meshes.set(part.id, mesh);
        c.root.add(mesh);
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

  // Selection, change highlight and x-ray body.
  useEffect(() => {
    const c = ctx.current;
    if (!c) return;
    for (const [id, mesh] of c.meshes) {
      const mat = mesh.material as THREE.MeshStandardMaterial;
      const isBody = mesh.userData.category === "body";
      const seeThrough = xray && isBody;
      if (mat.transparent !== seeThrough) mat.needsUpdate = true; // recompile the shader
      mat.transparent = seeThrough;
      mat.opacity = seeThrough ? 0.22 : 1;
      mat.depthWrite = !seeThrough;
      mat.emissive.set(id === selected ? 0x3d6fb6 : highlighted.includes(id) ? 0x7a5a12 : 0x000000);
    }
  }, [model, selected, highlighted, xray]);

  return (
    <>
      <div className="viewport" ref={host} />
      {animation && (
        <div className="playback">
          <span ref={label}>{animation.label}</span>
          <button onClick={onStop}>Stop</button>
        </div>
      )}
    </>
  );
}
