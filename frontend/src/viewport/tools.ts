import * as THREE from "three";

/** CAD viewer conventions (vehicle frame, ISO 8855: X forward, Y left, Z up). */
export type DisplayMode = "shaded" | "edges" | "wireframe" | "zebra" | "curvature";
export type StandardView = "iso" | "front" | "back" | "left" | "right" | "top" | "bottom";
export type SectionAxis = "off" | "x" | "y" | "z";

/** Direction from the target to the camera, and the camera's up vector, for each view. */
export const VIEWS: Record<StandardView, { dir: THREE.Vector3; up: THREE.Vector3; label: string }> = {
  iso: { dir: new THREE.Vector3(0.62, -0.62, 0.48).normalize(), up: new THREE.Vector3(0, 0, 1), label: "Isometric" },
  front: { dir: new THREE.Vector3(1, 0, 0), up: new THREE.Vector3(0, 0, 1), label: "Front" },
  back: { dir: new THREE.Vector3(-1, 0, 0), up: new THREE.Vector3(0, 0, 1), label: "Back" },
  left: { dir: new THREE.Vector3(0, 1, 0), up: new THREE.Vector3(0, 0, 1), label: "Left" },
  right: { dir: new THREE.Vector3(0, -1, 0), up: new THREE.Vector3(0, 0, 1), label: "Right" },
  top: { dir: new THREE.Vector3(0, 0, 1), up: new THREE.Vector3(1, 0, 0), label: "Top" },
  bottom: { dir: new THREE.Vector3(0, 0, -1), up: new THREE.Vector3(1, 0, 0), label: "Bottom" },
};

/** Camera position that frames a box from a view direction with a vertical field of view. */
export function framing(box: THREE.Box3, view: StandardView, fovDeg: number, aspect: number) {
  const centre = box.getCenter(new THREE.Vector3());
  const radius = box.getBoundingSphere(new THREE.Sphere()).radius || 1;
  const fov = THREE.MathUtils.degToRad(fovDeg);
  const fit = Math.max(radius / Math.sin(fov / 2), radius / Math.sin(Math.atan(Math.tan(fov / 2) * aspect)));
  const { dir, up } = VIEWS[view];
  return { target: centre, position: centre.clone().addScaledVector(dir, fit * 1.05), up: up.clone(), radius };
}

/** Section plane through the model box: keeps the side below ``share`` along the axis. */
export function sectionPlane(box: THREE.Box3, axis: Exclude<SectionAxis, "off">, share: number): THREE.Plane {
  const i = { x: 0, y: 1, z: 2 }[axis];
  const lo = box.min.getComponent(i), hi = box.max.getComponent(i);
  const at = lo + (hi - lo) * Math.min(Math.max(share, 0), 1);
  const normal = new THREE.Vector3().setComponent(i, -1); // keep coordinates below ``at``
  return new THREE.Plane(normal, at);
}

/** Distance between two picked points, mm, with its components along X, Y and Z. */
export function measure(a: THREE.Vector3, b: THREE.Vector3) {
  const d = b.clone().sub(a);
  return { distance: d.length(), dx: Math.abs(d.x), dy: Math.abs(d.y), dz: Math.abs(d.z) };
}

/** Feature edges of a mesh: CAD-style outline where faces meet at more than ``angle``. */
export function edgesOf(geometry: THREE.BufferGeometry, angle = 28): THREE.EdgesGeometry {
  return new THREE.EdgesGeometry(geometry, angle);
}

/** Line object drawing the given edges; it never takes a pick from the surface under it. */
export function featureEdges(edges: THREE.BufferGeometry): THREE.LineSegments {
  const lines = new THREE.LineSegments(
    edges, new THREE.LineBasicMaterial({ color: 0x0b0e12, transparent: true, opacity: 0.85 }),
  );
  lines.userData.edges = true;
  lines.raycast = () => {};
  return lines;
}

/**
 * Per-vertex curvature estimate for a display mesh (no CAD meaning beyond the mesh): at
 * each vertex, the largest angle between adjacent face normals divided by the mean length
 * of the edges there (1/mm). Coincident vertices are merged first, so seams between faces
 * count as the crease they are. Returns one value per vertex of ``geometry``.
 */
export function curvatureEstimate(geometry: THREE.BufferGeometry): Float32Array {
  const pos = geometry.getAttribute("position") as THREE.BufferAttribute;
  const index = geometry.getIndex();
  const n = pos.count;
  const tri = index ? Array.from(index.array as ArrayLike<number>) : Array.from({ length: n }, (_, i) => i);
  // Merge coincident vertices (positions rounded to 1 µm).
  const key = (i: number) => `${Math.round(pos.getX(i) * 1000)},${Math.round(pos.getY(i) * 1000)},${Math.round(pos.getZ(i) * 1000)}`;
  const ids = new Map<string, number>();
  const merged = new Int32Array(n);
  for (let i = 0; i < n; i++) {
    const k = key(i);
    let id = ids.get(k);
    if (id === undefined) { id = ids.size; ids.set(k, id); }
    merged[i] = id;
  }
  const m = ids.size;
  const faces: number[][] = Array.from({ length: m }, () => []);
  const edgeSum = new Float64Array(m), edgeCount = new Uint32Array(m);
  const normals: THREE.Vector3[] = [];
  const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
  for (let t = 0; t + 2 < tri.length; t += 3) {
    const [i, j, k] = [tri[t], tri[t + 1], tri[t + 2]];
    a.fromBufferAttribute(pos, i); b.fromBufferAttribute(pos, j); c.fromBufferAttribute(pos, k);
    const normal = new THREE.Vector3().subVectors(b, a).cross(new THREE.Vector3().subVectors(c, a));
    if (normal.lengthSq() < 1e-18) continue; // degenerate triangle
    normals.push(normal.normalize());
    const f = normals.length - 1;
    const corners: [number, THREE.Vector3, THREE.Vector3][] = [[i, a, b], [j, b, c], [k, c, a]];
    for (const [p, from, to] of corners) {
      const v = merged[p];
      faces[v].push(f);
      edgeSum[v] += from.distanceTo(to);
      edgeCount[v] += 1;
    }
  }
  const perMerged = new Float32Array(m);
  for (let v = 0; v < m; v++) {
    const fs = faces[v];
    let worst = 0;
    for (let x = 0; x < fs.length; x++) {
      for (let y = x + 1; y < fs.length; y++) {
        worst = Math.max(worst, normals[fs[x]].angleTo(normals[fs[y]]));
      }
    }
    perMerged[v] = edgeCount[v] ? worst / (edgeSum[v] / edgeCount[v]) : 0;
  }
  const out = new Float32Array(n);
  for (let i = 0; i < n; i++) out[i] = perMerged[merged[i]];
  return out;
}

/** Blue (flat) through green and yellow to red (tight curve or crease), log scale. */
export function curvatureColors(curvature: Float32Array): Float32Array {
  const colors = new Float32Array(curvature.length * 3);
  const lo = Math.log10(1e-4), hi = Math.log10(0.2); // 1/mm: radius about 10 m to 5 mm
  const col = new THREE.Color();
  for (let i = 0; i < curvature.length; i++) {
    const t = curvature[i] <= 0 ? 0 : Math.min(Math.max((Math.log10(curvature[i]) - lo) / (hi - lo), 0), 1);
    col.setHSL(0.66 * (1 - t), 0.85, 0.5);
    colors.set([col.r, col.g, col.b], i * 3);
  }
  return colors;
}
