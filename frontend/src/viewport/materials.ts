import * as THREE from "three";

export type Finish = "paint" | "glass" | "lamp" | "rubber" | "metal";

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
    default:
      return new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.42, metalness: 0.15,
        clearcoat: 0.6, clearcoatRoughness: 0.25 });
  }
}

/** Emissive the part shows when it is neither selected nor highlighted. */
export function baseEmissive(material: THREE.MeshStandardMaterial): THREE.Color {
  return (material.userData.baseEmissive as THREE.Color | undefined) ?? new THREE.Color(0);
}

export function rememberEmissive(material: THREE.MeshStandardMaterial): void {
  material.userData.baseEmissive = material.emissive.clone();
}
