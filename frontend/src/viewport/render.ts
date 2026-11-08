import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { EffectComposer } from "three/addons/postprocessing/EffectComposer.js";
import { OutputPass } from "three/addons/postprocessing/OutputPass.js";
import { RenderPass } from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/addons/postprocessing/UnrealBloomPass.js";

/** Look-development ("Render") mode, like the real-time render preview of a 3D suite: the
 * car in a photo studio or outdoors in daylight, with soft shadows, image-based reflections,
 * a ground fading into the backdrop, bloom on lit lamps, filmic tone mapping and
 * multisampling. Display only: no CAD meaning. Model units are millimetres. */
export type Look = "studio" | "outdoor";

export interface Studio {
  /** Turn the studio on or off in a look, framing ground, light and shadow on the model. */
  set(on: boolean, box: THREE.Box3, look?: Look): void;
  readonly on: boolean;
  /** Render a frame through the studio passes (only when on). */
  render(camera: THREE.Camera): void;
  resize(width: number, height: number, pixelRatio: number): void;
  dispose(): void;
}

interface LookSpec {
  exposure: number;
  environment: number; // reflections and ambient from the environment map
  key: { color: number; intensity: number; elevation: number; azimuth: number };
  fill: { sky: number; ground: number; intensity: number };
  ground: { color: number; roughness: number; specular: number; env: number };
  horizon: number; // fog colour where the ground meets the backdrop
  fog: [number, number]; // near, far (mm)
  backdrop: [string, number][]; // vertical gradient stops (top to bottom)
}

/** The two looks (exported for tests). */
export const LOOKS: Record<Look, LookSpec> = {
  studio: {
    exposure: 0.9, environment: 0.5,
    key: { color: 0xffffff, intensity: 1.5, elevation: 62, azimuth: -35 },
    fill: { sky: 0xe8eef6, ground: 0x08090b, intensity: 0.35 },
    ground: { color: 0x0e1013, roughness: 0.62, specular: 0.18, env: 0.12 },
    horizon: 0x15181c, fog: [9000, 26000],
    backdrop: [["#3a414b", 0], ["#15181c", 0.62], ["#15181c", 1]],
  },
  outdoor: { // late-afternoon sun by the sea: blue sky, warm low sun, stone paving
    exposure: 0.95, environment: 0.85,
    key: { color: 0xffe2b8, intensity: 2.4, elevation: 32, azimuth: -55 },
    fill: { sky: 0x9fb8d8, ground: 0x6a6258, intensity: 0.55 },
    ground: { color: 0x8a8174, roughness: 0.92, specular: 0.3, env: 0.35 },
    horizon: 0xb9c3cc, fog: [14000, 60000],
    backdrop: [["#4d6f9c", 0], ["#8fa9c6", 0.38], ["#c9d3db", 0.6], ["#b9c3cc", 1]],
  },
};

export const BLOOM = { strength: 0.32, radius: 0.25, threshold: 2.4 }; // lit lamps, not sun glints

/** A vertical backdrop gradient with a soft vignette. */
export function backdrop(stops: [string, number][], width = 512, height = 512): HTMLCanvasElement {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const g = canvas.getContext("2d");
  if (!g) return canvas;
  const sky = g.createLinearGradient(0, 0, 0, height);
  for (const [colour, at] of stops) sky.addColorStop(at, colour);
  g.fillStyle = sky;
  g.fillRect(0, 0, width, height);
  const glow = g.createRadialGradient(width / 2, height * 0.45, 0, width / 2, height * 0.45, width * 0.75);
  glow.addColorStop(0, "rgba(255,255,255,0.08)");
  glow.addColorStop(1, "rgba(0,0,0,0.25)");
  g.fillStyle = glow;
  g.fillRect(0, 0, width, height);
  return canvas;
}

/** Stone paving (offset rows of irregular setts with grout lines), drawn on a canvas that
 * tiles; one tile is ``PAVING_TILE`` mm square. */
export const PAVING_TILE = 2200;

export function paving(size = 1024, seed = 7): HTMLCanvasElement {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = size;
  const g = canvas.getContext("2d");
  if (!g) return canvas;
  let state = seed;
  const rand = () => ((state = (state * 16807) % 2147483647) / 2147483647);
  g.fillStyle = "#4a443c"; // grout
  g.fillRect(0, 0, size, size);
  const rows = 12;
  const h = size / rows;
  for (let r = 0; r < rows; r++) {
    let x = -rand() * h;
    while (x < size) {
      const w = h * (0.9 + rand() * 0.9);
      const tone = 118 + Math.round(rand() * 46);
      g.fillStyle = `rgb(${tone + 8},${tone},${tone - 12})`;
      const gap = size / 340;
      g.beginPath();
      g.roundRect(x + gap, r * h + gap, w - 2 * gap, h - 2 * gap, h * 0.12);
      g.fill();
      if (x + w > size) { // wrap the stone that runs off the right edge, so the tile repeats
        g.beginPath();
        g.roundRect(x + gap - size, r * h + gap, w - 2 * gap, h - 2 * gap, h * 0.12);
        g.fill();
      }
      x += w;
    }
  }
  const grain = g.getImageData(0, 0, size, size);
  for (let i = 0; i < grain.data.length; i += 4) {
    const n = (rand() - 0.5) * 22;
    grain.data[i] += n; grain.data[i + 1] += n; grain.data[i + 2] += n;
  }
  g.putImageData(grain, 0, 0);
  return canvas;
}

/** Ground and shadow frustum half-size for a model box, mm. */
export function studioExtent(box: THREE.Box3): { centre: THREE.Vector3; half: number } {
  const centre = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  return { centre, half: Math.max(size.x, size.y, 2000) * 0.75 + 600 };
}

/** Daylight for reflections: a sky dome (deep blue overhead, pale at the horizon), a bright
 * sun and warm ground below the horizon, rendered into an environment map. Z up. */
export function daylightScene(sunAzimuthDeg: number, sunElevationDeg: number): THREE.Scene {
  const scene = new THREE.Scene();
  const dome = new THREE.Mesh(new THREE.SphereGeometry(100, 48, 24), new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false,
    uniforms: {
      zenith: { value: new THREE.Color(0x2c5aa0) }, horizon: { value: new THREE.Color(0xd8e2ea) },
      ground: { value: new THREE.Color(0x5d554c) },
    },
    vertexShader: "varying vec3 vDir; void main() { vDir = normalize(position); "
      + "gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
    fragmentShader: "uniform vec3 zenith; uniform vec3 horizon; uniform vec3 ground; varying vec3 vDir; "
      + "void main() { float h = vDir.z; vec3 c = h > 0.0 ? mix(horizon, zenith, pow(h, 0.55)) "
      + ": mix(horizon * 0.6, ground, min(-h * 6.0, 1.0)); gl_FragColor = vec4(c, 1.0); }",
  }));
  scene.add(dome);
  const az = THREE.MathUtils.degToRad(sunAzimuthDeg), el = THREE.MathUtils.degToRad(sunElevationDeg);
  const sun = new THREE.Mesh(new THREE.SphereGeometry(4, 16, 8),
    new THREE.MeshBasicMaterial({ color: new THREE.Color(0xfff1d6).multiplyScalar(40) }));
  sun.position.set(90 * Math.cos(el) * Math.cos(az), 90 * Math.cos(el) * Math.sin(az), 90 * Math.sin(el));
  scene.add(sun);
  return scene;
}

export function createStudio(renderer: THREE.WebGLRenderer, scene: THREE.Scene, hide: THREE.Object3D[]): Studio {
  const group = new THREE.Group();
  group.visible = false;
  scene.add(group);

  // The ground catches the soft shadow and fades into the backdrop with distance (fog).
  // Low specular: a glossy ground mirrors the bright environment at grazing angles.
  const groundMaterial = new THREE.MeshPhysicalMaterial({ metalness: 0 });
  const ground = new THREE.Mesh(new THREE.CircleGeometry(80000, 96), groundMaterial);
  ground.receiveShadow = true;
  ground.position.z = -0.5;
  group.add(ground);
  const fog = new THREE.Fog(0, 1, 2);
  const stones = new THREE.CanvasTexture(paving());
  stones.colorSpace = THREE.SRGBColorSpace;
  stones.wrapS = stones.wrapT = THREE.RepeatWrapping;
  stones.repeat.set(160000 / PAVING_TILE, 160000 / PAVING_TILE); // the ground disc is 160 m across
  stones.anisotropy = renderer.capabilities.getMaxAnisotropy();

  // Key light (studio soft box, or the sun) casting soft shadows; a cool rim; a fill.
  const key = new THREE.DirectionalLight(0xffffff, 1);
  key.castShadow = true;
  key.shadow.mapSize.set(4096, 4096);
  key.shadow.bias = -0.0002;
  key.shadow.normalBias = 3;
  key.shadow.radius = 6;
  group.add(key, key.target);
  const rim = new THREE.DirectionalLight(0xcfd8ff, 0.9);
  group.add(rim, rim.target);
  const fill = new THREE.HemisphereLight(0xffffff, 0x000000, 0.3);
  group.add(fill);

  const pmrem = new THREE.PMREMGenerator(renderer);
  const environments: Record<Look, THREE.Texture> = {
    studio: pmrem.fromScene(new RoomEnvironment(), 0.02).texture,
    outdoor: pmrem.fromScene(daylightScene(LOOKS.outdoor.key.azimuth, LOOKS.outdoor.key.elevation), 0.01).texture,
  };
  pmrem.dispose();
  const backdropTexture = (l: Look) => {
    const t = new THREE.CanvasTexture(backdrop(LOOKS[l].backdrop));
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  };
  const backdrops: Record<Look, THREE.Texture> = { studio: backdropTexture("studio"), outdoor: backdropTexture("outdoor") };

  const target = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, target);
  const pass = new RenderPass(scene, new THREE.PerspectiveCamera());
  const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), BLOOM.strength, BLOOM.radius, BLOOM.threshold);
  composer.addPass(pass);
  composer.addPass(bloom);
  composer.addPass(new OutputPass());
  if (import.meta.env.DEV) (window as unknown as { __studio: unknown }).__studio = { bloom, key, ground };

  let on = false;
  let look: Look = "studio";
  let saved: { environment: THREE.Texture | null; intensity: number;
    background: THREE.Scene["background"]; exposure: number; fog: THREE.Scene["fog"] } | null = null;
  const casters = (enable: boolean) => scene.traverse((o) => {
    if ((o as THREE.Mesh).isMesh && !group.children.includes(o)) {
      o.castShadow = enable;
      o.receiveShadow = enable;
    }
  });

  const apply = (box: THREE.Box3) => {
    const spec = LOOKS[look];
    scene.environment = environments[look];
    scene.environmentIntensity = spec.environment;
    scene.background = backdrops[look];
    renderer.toneMappingExposure = spec.exposure;
    fog.color.set(spec.horizon);
    [fog.near, fog.far] = spec.fog;
    scene.fog = fog;
    groundMaterial.color.set(look === "outdoor" ? 0xffffff : spec.ground.color);
    const map = look === "outdoor" ? stones : null;
    if (groundMaterial.map !== map) { groundMaterial.map = map; groundMaterial.needsUpdate = true; }
    groundMaterial.roughness = spec.ground.roughness;
    groundMaterial.specularIntensity = spec.ground.specular;
    groundMaterial.envMapIntensity = spec.ground.env;
    key.color.set(spec.key.color);
    key.intensity = spec.key.intensity;
    fill.color.set(spec.fill.sky);
    fill.groundColor.set(spec.fill.ground);
    fill.intensity = spec.fill.intensity;
    if (box.isEmpty()) return;
    const { centre, half } = studioExtent(box);
    const az = THREE.MathUtils.degToRad(spec.key.azimuth), el = THREE.MathUtils.degToRad(spec.key.elevation);
    const reach = half * 2.4;
    key.position.set(centre.x + reach * Math.cos(el) * Math.cos(az),
      centre.y + reach * Math.cos(el) * Math.sin(az), reach * Math.sin(el));
    key.target.position.set(centre.x, centre.y, 0);
    const cam = key.shadow.camera;
    cam.left = cam.bottom = -half;
    cam.right = cam.top = half;
    cam.near = 10;
    cam.far = reach * 2.5;
    cam.updateProjectionMatrix();
    rim.position.set(centre.x - half, centre.y + half, half);
    rim.target.position.copy(centre);
  };

  return {
    get on() { return on; },
    set(next: boolean, box: THREE.Box3, nextLook: Look = look) {
      if (next && !on) {
        saved = { environment: scene.environment, intensity: scene.environmentIntensity,
          background: scene.background, exposure: renderer.toneMappingExposure, fog: scene.fog };
      }
      if (!next && on && saved) {
        scene.environment = saved.environment;
        scene.environmentIntensity = saved.intensity;
        scene.background = saved.background;
        renderer.toneMappingExposure = saved.exposure;
        scene.fog = saved.fog;
      }
      on = next;
      look = nextLook;
      group.visible = on;
      for (const o of hide) o.visible = !on;
      renderer.shadowMap.enabled = on;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      if (on) apply(box);
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
      for (const t of Object.values(environments)) t.dispose();
      for (const t of Object.values(backdrops)) t.dispose();
      stones.dispose();
      ground.geometry.dispose();
      groundMaterial.dispose();
      scene.remove(group);
    },
  };
}
