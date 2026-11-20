import { describe, expect, it } from "vitest";
import { otsu, thin, toGrey, traceEnclosed } from "./traceSketch";

/** A white bitmap with dark pen strokes drawn into it. */
function paper(w: number, h: number) {
  const g = new Uint8Array(w * h).fill(235);
  const pen = (x: number, y: number, r = 1.5) => {
    for (let dy = -2; dy <= 2; dy += 1) for (let dx = -2; dx <= 2; dx += 1) {
      const px = Math.round(x + dx), py = Math.round(y + dy);
      if (dx * dx + dy * dy <= r * r && px >= 0 && py >= 0 && px < w && py < h) g[py * w + px] = 30;
    }
  };
  return { g, pen };
}

describe("trace a paper sketch", () => {
  it("finds Otsu's threshold between ink and paper", () => {
    const g = new Uint8Array(100).map((_, i) => (i < 20 ? 25 : 230));
    const t = otsu(g);
    expect(t).toBeGreaterThanOrEqual(25);
    expect(t).toBeLessThan(230);
  });

  it("converts RGBA to grey with transparency as paper", () => {
    const rgba = new Uint8ClampedArray([0, 0, 0, 255, 0, 0, 0, 0]);
    expect(Array.from(toGrey(rgba, 2, 1))).toEqual([0, 255]);
  });

  it("traces the inside of a drawn rectangle and a circle drawn inside it", () => {
    const w = 200, h = 140;
    const { g, pen } = paper(w, h);
    for (let x = 20; x <= 180; x += 0.5) { pen(x, 20); pen(x, 120); }
    for (let y = 20; y <= 120; y += 0.5) { pen(20, y); pen(180, y); }
    for (let t = 0; t < 2 * Math.PI; t += 0.01) pen(70 + 18 * Math.cos(t), 70 + 18 * Math.sin(t));
    const loops = traceEnclosed(g, w, h);
    expect(loops.length).toBe(2); // the plate area, then the hole
    const [outer, hole] = loops;
    const xs = outer.map((p) => p[0]), ys = outer.map((p) => p[1]);
    expect(Math.min(...xs)).toBeGreaterThan(20);
    expect(Math.max(...xs)).toBeLessThan(180);
    expect(Math.max(...xs) - Math.min(...xs)).toBeGreaterThan(150); // half a pen inside
    expect(Math.max(...ys) - Math.min(...ys)).toBeGreaterThan(90);
    const r = hole.reduce((s, [x, y]) => s + Math.hypot(x - 70, y - 70), 0) / hole.length;
    expect(r).toBeGreaterThan(14);
    expect(r).toBeLessThan(18);
    expect(thin(outer, 4).length).toBeLessThan(outer.length);
  });

  it("ignores ink that encloses nothing and specks of dust", () => {
    const w = 100, h = 80;
    const { g, pen } = paper(w, h);
    for (let x = 10; x <= 90; x += 0.5) pen(x, 40); // an open line
    g[5 * w + 5] = 0;
    expect(traceEnclosed(g, w, h)).toEqual([]);
  });
});
