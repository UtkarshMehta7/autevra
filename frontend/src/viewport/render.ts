import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";

/** Look-development ("Render") mode: a photo studio for judging surfaces and finishes, like
 * a real-time render preview in a 3D suite. Soft key light with soft shadows, a satin floor
 * fading into a studio backdrop, bloom on lit lamps, filmic tone mapping and multisampling. Display only: no CAD meaning.
 * Model units are millimetres. */
export interface Studio {
  /** Turn the studio on or off, framing the floor, light and shadow on the model box. */
  set(on: boolean, box: THREE.Box3): void;
  readonly on: boolean;
  /** Render a frame through the studio passes (only when on). */
  render(camera: THREE.Camera): void;
  resize(width: number, height: number, pixelRatio: number): void;
  dispose(): void;
}

/** Studio settings, exported for tests. */
export const STUDIO = {
  exposure: 0.85,
  environment: 0.55,
  keyIntensity: 2.6,
  bloom: { strength: 0.28, radius: 0.25, threshold: 0.96 },
} as const;

const FLOOR = 0x202328;
const HORIZON = 0x15181c; // the backdrop colour at the floor line (fog colour)

/** A vertical backdrop gradient with a soft vignette, as a photo studio cyclorama. */
export function backdrop(width = 512, height = 512): HTMLCanvasElement {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const g = canvas.getContext("2d");
  if (!g) return canvas;
  const sky = g.createLinearGradient(0, 0, 0, height);
  sky.addColorStop(0, "#3a414b");
  sky.addColorStop(0.62, "#15181c");
  sky.addColorStop(1, "#15181c");
  g.fillStyle = sky;
  g.fillRect(0, 0, width, height);
  const glow = g.createRadialGradient(width / 2, height * 0.45, 0, width / 2, height * 0.45, width * 0.75);
  glow.addColorStop(0, "rgba(255,255,255,0.10)");
  glow.addColorStop(1, "rgba(0,0,0,0.35)");
  g.fillStyle = glow;
  g.fillRect(0, 0, width, height);
  return canvas;
}

/** Floor radius and shadow frustum half-size for a model box, mm. */
export function studioExtent(box: THREE.Box3): { centre: THREE.Vector3; half: number } {
  const centre = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  return { centre, half: Math.max(size.x, size.y, 2000) * 0.75 + 600 };
}

export function createStudio(renderer: THREE.WebGLRenderer, scene: THREE.Scene, hide: THREE.Object3D[]): Studio {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);

  // Satin studio floor: dark, catching the soft shadow and a sheen of the studio lights,
  // fading into the backdrop with distance (studio fog), so the car stands in a cyclorama.
  const floor = new THREE.Mesh(new THREE.CircleGeometry(60000, 96), new THREE.MeshStandardMaterial({
    color: FLOOR, roughness: 0.48, metalness: 0, envMapIntensity: 0.35,
  }));
  floor.receiveShadow = true;
  floor.position.z = -0.5;
  group.add(floor);
  const fog = new THREE.Fog(HORIZON, 12000, 40000);

  // Key light: a large soft source above and slightly ahead, casting soft shadows.
  const key = new THREE.DirectionalLight(0xffffff, STUDIO.keyIntensity);
  key.castShadow = true;
  key.shadow.mapSize.set(4096, 4096);
  key.shadow.bias = -0.0002;
  key.shadow.normalBias = 3;
  key.shadow.radius = 6;
  group.add(key, key.target);
  const rim = new THREE.DirectionalLight(0xcfd8ff, 0.9); // cool rim from behind
  group.add(rim, rim.target);

  const pmrem = new THREE.PMREMGenerator(renderer);
  const environment = pmrem.fromScene(new RoomEnvironment(), 0.02).texture;
  pmrem.dispose();
  const background = new THREE.CanvasTexture(backdrop());
  background.colorSpace = THREE.SRGBColorSpace;

  const target = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, target);
  const camera0 = new THREE.PerspectiveCamera();
  const pass = new RenderPass(scene, camera0);
  const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), STUDIO.bloom.strength,
    STUDIO.bloom.radius, STUDIO.bloom.threshold);
  composer.addPass(pass);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());
  if (import.meta.env.DEV) (window as unknown as { __studio: unknown }).__studio = { bloom, key, floor };

  let on = false;
  const saved = { environment: scene.environment, intensity: scene.environmentIntensity,
    background: scene.background, exposure: renderer.toneMappingExposure, fog: scene.fog };
  const casters = (enable: boolean) => scene.traverse((o) => {
    if ((o as THREE.Mesh).isMesh && !group.children.includes(o)) {
      o.castShadow = enable;
      o.receiveShadow = enable;
    }
  });

  return {
    get on() { return on; },
    set(next: boolean, box: THREE.Box3) {
      if (next && !box.isEmpty()) {
        const { centre, half } = studioExtent(box);
          key.position.set(centre.x + 0.35 * half, centre.y - 0.25 * half, half * 2.2);
        key.target.position.set(centre.x, centre.y, 0);
        const cam = key.shadow.camera;
        cam.left = cam.bottom = -half;
        cam.right = cam.top = half;
        cam.near = 10;
        cam.far = half * 5;
        cam.updateProjectionMatrix();
        rim.position.set(centre.x - half, centre.y + half, half);
        rim.target.position.copy(centre);
      }
      if (next === on) { casters(on); return; }
      on = next;
      group.visible = on;
      for (const o of hide) o.visible = !on;
      renderer.shadowMap.enabled = on;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      if (on) {
        Object.assign(saved, { environment: scene.environment, intensity: scene.environmentIntensity,
          background: scene.background, exposure: renderer.toneMappingExposure, fog: scene.fog });
        scene.fog = fog;
        scene.environment = environment;
        scene.environmentIntensity = STUDIO.environment;
        scene.background = background;
        renderer.toneMappingExposure = STUDIO.exposure;
      } else {
        scene.environment = saved.environment;
        scene.environmentIntensity = saved.intensity;
        scene.background = saved.background;
        renderer.toneMappingExposure = saved.exposure;
        scene.fog = saved.fog;
      }
      casters(on);
    },
    render(camera: THREE.Camera) {
      pass.camera = camera;
      composer.render();
    },
    resize(width: number, height: number, pixelRatio: number) {
      composer.setPixelRatio(pixelRatio);
      composer.setSize(Math.max(width, 1), Math.max(height, 1));
    },
    dispose() {
      composer.dispose();
      target.dispose();
      environment.dispose();
      background.dispose();
      floor.geometry.dispose();
      (floor.material as THREE.Material).dispose();
      scene.remove(group);
    },
  };
}
