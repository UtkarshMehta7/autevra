import * as THREE from "three";

/**
 * Smooth vertex normals that keep real edges crisp, weighted by the corner angle of each
 * triangle at the vertex (Thürmer and Wüthrich). Unlike equal or area weights, angle
 * weights do not depend on how a quad was split into two triangles, so the long, thin
 * facets of a ruled loft shade evenly instead of zig-zagging in highlight lines.
 *
 * Vertices at the same position (B-rep face seams send them separately) are shared; a
 * neighbouring triangle contributes only when its normal is within ``crease`` radians of
 * this triangle's normal. Returns a non-indexed geometry with one normal per corner.
 */
export function creasedAngleNormals(vertices: ArrayLike<number>, indices: ArrayLike<number>,
  crease: number): THREE.BufferGeometry {
  const tris = indices.length / 3;
  const face = new Float32Array(tris * 3);
  const angle = new Float32Array(tris * 3);
  const key = new Int32Array(indices.length);
  const ids = new Map<string, number>();
  const q = (v: number) => Math.round(v * 1000); // 1 micrometre in model mm
  for (let c = 0; c < indices.length; c++) {
    const i = indices[c] * 3;
    const k = `${q(vertices[i])},${q(vertices[i + 1])},${q(vertices[i + 2])}`;
    let id = ids.get(k);
    if (id === undefined) { id = ids.size; ids.set(k, id); }
    key[c] = id;
  }
  const p = [new THREE.Vector3(), new THREE.Vector3(), new THREE.Vector3()];
  const e1 = new THREE.Vector3(), e2 = new THREE.Vector3(), n = new THREE.Vector3();
  for (let t = 0; t < tris; t++) {
    for (let j = 0; j < 3; j++) p[j].fromArray(vertices as number[], indices[3 * t + j] * 3);
    n.subVectors(p[1], p[0]).cross(e1.subVectors(p[2], p[0]));
    const len = n.length();
    if (len > 0) n.divideScalar(len);
    face.set([n.x, n.y, n.z], 3 * t);
    for (let j = 0; j < 3; j++) {
      e1.subVectors(p[(j + 1) % 3], p[j]);
      e2.subVectors(p[(j + 2) % 3], p[j]);
      angle[3 * t + j] = len > 0 ? e1.angleTo(e2) : 0;
    }
  }
  // corners at each shared position (compressed adjacency)
  const start = new Int32Array(ids.size + 1);
  for (let c = 0; c < key.length; c++) start[key[c] + 1]++;
  for (let v = 0; v < ids.size; v++) start[v + 1] += start[v];
  const fill = start.slice(0, ids.size);
  const corners = new Int32Array(key.length);
  for (let c = 0; c < key.length; c++) corners[fill[key[c]]++] = c;

  const cos = Math.cos(crease);
  const position = new Float32Array(indices.length * 3);
  const normal = new Float32Array(indices.length * 3);
  for (let c = 0; c < indices.length; c++) {
    const i = indices[c] * 3;
    position[3 * c] = vertices[i];
    position[3 * c + 1] = vertices[i + 1];
    position[3 * c + 2] = vertices[i + 2];
    const t = Math.floor(c / 3);
    const fx = face[3 * t], fy = face[3 * t + 1], fz = face[3 * t + 2];
    let sx = 0, sy = 0, sz = 0;
    for (let a = start[key[c]]; a < start[key[c] + 1]; a++) {
      const other = corners[a], u = Math.floor(other / 3);
      const ox = face[3 * u], oy = face[3 * u + 1], oz = face[3 * u + 2];
      if (fx * ox + fy * oy + fz * oz < cos) continue;
      const w = angle[other];
      sx += w * ox; sy += w * oy; sz += w * oz;
    }
    const l = Math.hypot(sx, sy, sz) || 1;
    normal[3 * c] = l > 1e-12 ? sx / l : fx;
    normal[3 * c + 1] = l > 1e-12 ? sy / l : fy;
    normal[3 * c + 2] = l > 1e-12 ? sz / l : fz;
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(position, 3));
  g.setAttribute("normal", new THREE.BufferAttribute(normal, 3));
  return g;
}
