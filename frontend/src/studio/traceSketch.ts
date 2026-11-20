/** Trace a photo or scan of a pen sketch into closed loops.
 *
 * A pen drawing is read by the areas its ink encloses: the image is turned to grey, split
 * into ink and paper by Otsu's threshold, the paper is labelled into connected areas, and
 * every area that does not touch the image border (the inside of an outline, the inside of
 * a hole drawn within it) has its outer boundary traced (Moore neighbour tracing). The
 * loops lie half a pen width inside the drawn lines, whatever the pen, and go to the same
 * cleanup as strokes drawn on screen. */

export type Loop = [number, number][];

export function toGrey(rgba: Uint8ClampedArray, w: number, h: number): Uint8Array {
  const g = new Uint8Array(w * h);
  for (let i = 0; i < w * h; i += 1) {
    const a = rgba[4 * i + 3] / 255; // transparent counts as paper (white)
    const v = 0.299 * rgba[4 * i] + 0.587 * rgba[4 * i + 1] + 0.114 * rgba[4 * i + 2];
    g[i] = Math.round(v * a + 255 * (1 - a));
  }
  return g;
}

/** Otsu's threshold: the grey level that best separates ink from paper. */
export function otsu(grey: Uint8Array): number {
  const hist = new Array<number>(256).fill(0);
  for (const v of grey) hist[v] += 1;
  const total = grey.length;
  let sum = 0;
  for (let i = 0; i < 256; i += 1) sum += i * hist[i];
  let sumB = 0, wB = 0, best = 0, threshold = 128;
  for (let t = 0; t < 256; t += 1) {
    wB += hist[t];
    if (!wB) continue;
    const wF = total - wB;
    if (!wF) break;
    sumB += t * hist[t];
    const mB = sumB / wB, mF = (sum - sumB) / wF;
    const between = wB * wF * (mB - mF) ** 2;
    if (between > best) { best = between; threshold = t; }
  }
  return threshold;
}

/** Outer boundaries of the paper areas enclosed by ink, in pixel coordinates (y down),
 * largest first; areas under ``minArea`` pixels are noise and skipped. */
export function traceEnclosed(grey: Uint8Array, w: number, h: number, threshold = otsu(grey), minArea = 0.0015 * w * h): Loop[] {
  const ink = (i: number) => grey[i] <= threshold;
  const label = new Int32Array(w * h).fill(-1);
  const regions: { id: number; area: number; border: boolean; seed: number }[] = [];
  const stack: number[] = [];
  for (let start = 0; start < w * h; start += 1) {
    if (label[start] !== -1 || ink(start)) continue;
    const id = regions.length;
    let area = 0, border = false;
    label[start] = id;
    stack.push(start);
    while (stack.length) {
      const i = stack.pop()!;
      area += 1;
      const x = i % w, y = (i - x) / w;
      if (x === 0 || y === 0 || x === w - 1 || y === h - 1) border = true;
      for (const j of [x > 0 ? i - 1 : -1, x < w - 1 ? i + 1 : -1, y > 0 ? i - w : -1, y < h - 1 ? i + w : -1]) {
        if (j >= 0 && label[j] === -1 && !ink(j)) { label[j] = id; stack.push(j); }
      }
    }
    regions.push({ id, area, border, seed: start });
  }
  const loops: { loop: Loop; area: number }[] = [];
  for (const r of regions) {
    if (r.border || r.area < minArea) continue;
    loops.push({ loop: moore(label, w, h, r.id, r.seed), area: r.area });
  }
  return loops.sort((a, b) => b.area - a.area).map((l) => l.loop);
}

// Moore neighbour tracing of a region's outer boundary from its top-left pixel (the scan
// order reaches the region first at its top-left, so its west neighbour is outside).
const DIRS: [number, number][] = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]];

function moore(label: Int32Array, w: number, h: number, id: number, seed: number): Loop {
  const inside = (x: number, y: number) => x >= 0 && y >= 0 && x < w && y < h && label[y * w + x] === id;
  const sx = seed % w, sy = (seed - sx) / w;
  const out: Loop = [[sx + 0.5, sy + 0.5]];
  let x = sx, y = sy, back = 4; // came from the west
  for (let steps = 0; steps < 4 * w * h; steps += 1) {
    let found = false;
    for (let k = 1; k <= 8; k += 1) {
      const d = (back + k) % 8;
      const nx = x + DIRS[d][0], ny = y + DIRS[d][1];
      if (inside(nx, ny)) {
        x = nx; y = ny; back = (d + 4) % 8;
        found = true;
        break;
      }
    }
    if (!found) break; // a single pixel
    if (x === sx && y === sy) break;
    out.push([x + 0.5, y + 0.5]);
  }
  return out;
}

/** Every n-th point of a loop, closed again. */
export function thin(loop: Loop, step: number): Loop {
  const out = loop.filter((_, i) => i % Math.max(1, step) === 0);
  return out.length > 2 ? [...out, out[0]] : loop;
}
