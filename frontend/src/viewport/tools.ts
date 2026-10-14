import * as THREE from "three";

/** CAD viewer conventions (vehicle frame, ISO 8855: X forward, Y left, Z up). */
export type DisplayMode = "shaded" | "edges" | "wireframe";
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
