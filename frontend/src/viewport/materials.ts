import * as THREE from "three";

export type Finish =
  | "paint" | "paint_gloss" | "paint_metallic" | "paint_matte" | "paint_pearl"
  | "glass" | "lamp" | "rubber" | "metal" | "leather" | "fabric" | "trim" | "screen";

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
