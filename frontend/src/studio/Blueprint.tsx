import { useEffect, useState } from "react";

/** A reference image placed in model units (mm): x from left edge, v of the top edge. */
export interface Blueprint {
  src: string; // downscaled data URL
  aspect: number; // height / width of the image
  x: number; // model x of the image's left edge
  v: number; // model v of the image's top edge
  width: number; // model width of the image, mm
  opacity: number;
  flip: boolean; // mirror horizontally (a car drawn facing right)
}

const KEY = (project: string, view: string) => `autevra.blueprint.${project}.${view}`;

export function loadBlueprint(project: string, view: string): Blueprint | null {
  try {
    const raw = localStorage.getItem(KEY(project, view));
    return raw ? (JSON.parse(raw) as Blueprint) : null;
  } catch {
    return null;
  }
}

export function saveBlueprint(project: string, view: string, bp: Blueprint | null): void {
  try {
    if (bp) localStorage.setItem(KEY(project, view), JSON.stringify(bp));
    else localStorage.removeItem(KEY(project, view));
  } catch {
    // storage full or blocked: the blueprint stays for this session only
  }
}

/** Read an image file, downscale it to at most 1600 px wide (JPEG) and measure it. */
export async function readImage(file: File): Promise<{ src: string; aspect: number }> {
  const url = URL.createObjectURL(file);
  try {
    const img = await new Promise<HTMLImageElement>((ok, fail) => {
      const i = new Image();
      i.onload = () => ok(i);
      i.onerror = () => fail(new Error("that file is not an image the browser can read"));
      i.src = url;
    });
    const scale = Math.min(1, 1600 / img.naturalWidth);
    const canvas = document.createElement("canvas");
    canvas.width = Math.round(img.naturalWidth * scale);
    canvas.height = Math.round(img.naturalHeight * scale);
    canvas.getContext("2d")!.drawImage(img, 0, 0, canvas.width, canvas.height);
    return { src: canvas.toDataURL("image/jpeg", 0.85), aspect: img.naturalHeight / img.naturalWidth };
  } finally {
    URL.revokeObjectURL(url);
  }
}

/** The image as an SVG element in model units (the editor flips v; we draw at -v). */
export function BlueprintImage({ bp }: { bp: Blueprint }) {
  const h = bp.width * bp.aspect;
  const transform = bp.flip ? `translate(${2 * bp.x + bp.width} 0) scale(-1 1)` : undefined;
  return (
    <image href={bp.src} x={bp.x} y={-bp.v} width={bp.width} height={h} opacity={bp.opacity}
      preserveAspectRatio="none" transform={transform} style={{ pointerEvents: "none" }} />
  );
}

/**
 * Controls for one view's blueprint: load, align on two reference points (the wheel
 * centres in the side view, the axle lines in the plan), opacity and mirroring.
 */
export function BlueprintControls({ project, view, bp, onChange, picking, onPickStart, label }: {
  project: string; view: string; bp: Blueprint | null; onChange: (bp: Blueprint | null) => void;
  picking: boolean; onPickStart: () => void; label: string;
}) {
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { saveBlueprint(project, view, bp); }, [project, view, bp]);
  return (
    <div className="blueprint-controls">
      <label className="button">Load {label} image
        <input type="file" accept="image/*" hidden onChange={async (ev) => {
          const file = ev.target.files?.[0];
          if (!file) return;
          try {
            const { src, aspect } = await readImage(file);
            onChange({ src, aspect, x: 0, v: 0, width: 0, opacity: 0.5, flip: false });
            setError(null);
          } catch (e) {
            setError(e instanceof Error ? e.message : String(e));
          }
        }} />
      </label>
      {bp && (
        <>
          <button className={picking ? "active" : ""} onClick={onPickStart}
            title="Click the front reference point, then the rear one, on the image">
            {picking ? "Click front, then rear…" : "Align on the wheels"}</button>
          <label>opacity<input type="range" min={0.1} max={1} step={0.05} value={bp.opacity}
            onChange={(e) => onChange({ ...bp, opacity: Number(e.target.value) })} /></label>
          <label><input type="checkbox" checked={bp.flip} onChange={(e) => onChange({ ...bp, flip: e.target.checked })} />mirror</label>
          <button onClick={() => onChange(null)}>Remove</button>
        </>
      )}
      {error && <span className="bad-text">{error}</span>}
    </div>
  );
}
