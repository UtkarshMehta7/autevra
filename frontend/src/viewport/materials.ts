import * as THREE from "three";

export type Finish =
  | "paint" | "paint_gloss" | "paint_metallic" | "paint_matte" | "paint_pearl"
  | "glass" | "lamp" | "rubber" | "metal" | "polished" | "leather" | "fabric" | "trim" | "screen";

/** Physically based display material for a part's finish (display only; no CAD meaning). */
export function materialFor(finish: string | undefined, color: [number, number, number]) {
  const c = new THREE.Color(...color);
  switch (finish as Finish | undefined) {
    case "glass": { // tinted and see-through, so the cabin shows
      const glass = new THREE.MeshPhysicalMaterial({ color: c, metalness: 0.1, roughness: 0.04,
        clearcoat: 1, clearcoatRoughness: 0.04, envMapIntensity: 1.6, transparent: true,
        opacity: 0.38, depthWrite: false });
      glass.userData.baseOpacity = 0.38;
      return glass;
    }
    case "leather":
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.55, metalness: 0,
        clearcoat: 0.25, clearcoatRoughness: 0.6, sheen: 0.3, sheenColor: c.clone() });
    case "fabric":
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.95, metalness: 0,
        sheen: 0.6, sheenRoughness: 0.8, sheenColor: c.clone().lerp(new THREE.Color(1, 1, 1), 0.2) });
    case "trim":
      return new THREE.MeshStandardMaterial({ color: c, roughness: 0.7, metalness: 0.05 });
    case "screen":
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.08, metalness: 0.2,
        clearcoat: 1, emissive: new THREE.Color(0.08, 0.22, 0.45), emissiveIntensity: 0.9 });
    case "lamp":
      return new THREE.MeshStandardMaterial({ color: c, roughness: 0.2, metalness: 0,
        emissive: c, emissiveIntensity: 0.55 });
    case "rubber":
      return new THREE.MeshStandardMaterial({ color: c, roughness: 0.92, metalness: 0 });
    case "polished": // diamond-cut or polished alloy
      return new THREE.MeshStandardMaterial({ color: c, roughness: 0.12, metalness: 1 });
    case "metal":
      return new THREE.MeshStandardMaterial({ color: c, roughness: 0.38, metalness: 0.75 });
    case "paint_metallic":
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.32, metalness: 0.65,
        clearcoat: 1, clearcoatRoughness: 0.08 });
    case "paint_matte":
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.78, metalness: 0.05,
        clearcoat: 0 });
    case "paint_pearl":
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.3, metalness: 0.3,
        clearcoat: 1, clearcoatRoughness: 0.05, iridescence: 0.35, iridescenceIOR: 1.5,
        sheen: 0.25, sheenColor: c.clone().lerp(new THREE.Color(1, 1, 1), 0.3) });
    default: // "paint", "paint_gloss": solid colour under clear coat
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.38, metalness: 0.08,
        clearcoat: 1, clearcoatRoughness: 0.06 });
  }
}

/** Emissive the part shows when it is neither selected nor highlighted. */
export function baseEmissive(material: THREE.MeshStandardMaterial): THREE.Color {
  return (material.userData.baseEmissive as THREE.Color | undefined) ?? new THREE.Color(0);
}

export function rememberEmissive(material: THREE.MeshStandardMaterial): void {
  material.userData.baseEmissive = material.emissive.clone();
}

/** Opacity the part has when not in X-ray (glass is see-through on its own). */
export function baseOpacity(material: THREE.Material): number {
  return (material.userData.baseOpacity as number | undefined) ?? 1;
}

let zebra: THREE.ShaderMaterial | null = null;

/** Highlight-line (zebra) analysis material: black and white bands reflected from a
 * striped environment fixed to the view. Smooth, continuous bands mean tangent- and
 * curvature-continuous surfaces; kinks and steps in the bands show breaks. Honours the
 * section plane. */
export function zebraMaterial(): THREE.ShaderMaterial {
  if (zebra) return zebra;
  zebra = new THREE.ShaderMaterial({
    clipping: true,
    side: THREE.DoubleSide,
    uniforms: { stripes: { value: 9.0 } },
    vertexShader: `
      #include <clipping_planes_pars_vertex>
      varying vec3 vNormal;
      varying vec3 vView;
      void main() {
        vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
        vNormal = normalize(normalMatrix * normal);
        vView = normalize(-mvPosition.xyz);
        gl_Position = projectionMatrix * mvPosition;
        #include <clipping_planes_vertex>
      }`,
    fragmentShader: `
      #include <clipping_planes_pars_fragment>
      uniform float stripes;
      varying vec3 vNormal;
      varying vec3 vView;
      void main() {
        #include <clipping_planes_fragment>
        vec3 n = normalize(vNormal);
        if (!gl_FrontFacing) n = -n;
        vec3 r = reflect(-normalize(vView), n);
        float t = fract(r.y * stripes);
        float w = fwidth(r.y * stripes) * 1.5;
        float band = smoothstep(0.5 - w, 0.5 + w, t) * (1.0 - smoothstep(1.0 - w, 1.0, t));
        gl_FragColor = vec4(mix(vec3(0.06), vec3(0.96), band), 1.0);
      }`,
  });
  return zebra;
}
