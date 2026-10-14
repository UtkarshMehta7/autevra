import * as THREE from "three";

export type Finish =
  | "paint" | "paint_gloss" | "paint_metallic" | "paint_matte" | "paint_pearl"
  | "glass" | "lamp" | "rubber" | "metal";

/** Physically based display material for a part's finish (display only; no CAD meaning). */
export function materialFor(finish: string | undefined, color: [number, number, number]) {
  const c = new THREE.Color(...color);
  switch (finish as Finish | undefined) {
    case "glass":
      return new THREE.MeshPhysicalMaterial({ color: c, metalness: 0.2, roughness: 0.05,
        clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 1.4 });
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
