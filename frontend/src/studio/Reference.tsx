import { useCallback, useEffect, useRef, useState } from "react";
import { readImage } from "./Blueprint";

/** Reference image beside the 3D view (as the reference images of a 3D suite): paste, drop or
 * load a photo of the design target and compare it with the model side by side. The image is
 * kept per project in this browser only. */
export interface ReferenceImage {
  src: string; // downscaled JPEG data URL
  aspect: number;
  name: string;
}

const KEY = (project: string) => `autevra.reference.${project}`;

export function loadReference(project: string): ReferenceImage | null {
  try {
    const raw = localStorage.getItem(KEY(project));
    return raw ? (JSON.parse(raw) as ReferenceImage) : null;
  } catch {
    return null;
  }
}

export function saveReference(project: string, image: ReferenceImage | null): void {
  try {
    if (image) localStorage.setItem(KEY(project), JSON.stringify(image));
    else localStorage.removeItem(KEY(project));
  } catch {
    // storage full or blocked: the image stays for this session only
  }
}

/** The first image file in a paste or drop, if any. */
export function imageFile(items: DataTransferItemList | null | undefined): File | null {
  for (const item of Array.from(items ?? [])) {
    if (item.kind === "file" && item.type.startsWith("image/")) return item.getAsFile();
  }
  return null;
}

interface Props {
  project: string;
  onClose: () => void;
}

export function ReferencePanel({ project, onClose }: Props) {
  const [image, setImage] = useState<ReferenceImage | null>(() => loadReference(project));
  const [error, setError] = useState<string | null>(null);
  const [over, setOver] = useState(false);
  const [mirror, setMirror] = useState(false);
  const input = useRef<HTMLInputElement>(null);

  useEffect(() => setImage(loadReference(project)), [project]);

  const take = useCallback(async (file: File | null) => {
    if (!file) return;
    try {
      const { src, aspect } = await readImage(file);
      const next = { src, aspect, name: file.name || "Pasted image" };
      setImage(next);
      saveReference(project, next);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  }, [project]);

  // Paste anywhere in the studio while the panel is open (not into a text field).
  useEffect(() => {
    const onPaste = (e: ClipboardEvent) => {
      const target = e.target as HTMLElement | null;
      if (target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA")) return;
      const file = imageFile(e.clipboardData?.items);
      if (file) { e.preventDefault(); void take(file); }
    };
    document.addEventListener("paste", onPaste);
    return () => document.removeEventListener("paste", onPaste);
  }, [take]);

  return (
    <aside className={`reference${over ? " over" : ""}`} aria-label="Reference image"
      onDragOver={(e) => { e.preventDefault(); setOver(true); }}
      onDragLeave={() => setOver(false)}
      onDrop={(e) => { e.preventDefault(); setOver(false); void take(imageFile(e.dataTransfer.items)); }}>
      <header>
        <strong>Reference</strong>
        <span className="muted" title={image?.name}>{image ? image.name : "none"}</span>
        <span className="spacer" />
        <button onClick={() => input.current?.click()} title="Load a photo from a file">Load…</button>
        <button className={mirror ? "on" : ""} onClick={() => setMirror(!mirror)} disabled={!image}
          title="Mirror the photo, to face the same way as the model">Mirror</button>
        <button onClick={() => { setImage(null); saveReference(project, null); }} disabled={!image}
          title="Remove the reference image">Clear</button>
        <button onClick={onClose} title="Close the reference panel" aria-label="Close">×</button>
        <input ref={input} type="file" accept="image/*" hidden
          onChange={(e) => { void take(e.target.files?.[0] ?? null); e.target.value = ""; }} />
      </header>
      {image ? (
        <img src={image.src} alt={`Reference: ${image.name}`} style={mirror ? { transform: "scaleX(-1)" } : undefined} />
      ) : (
        <div className="reference-empty">
          <p>Paste a photo (⌘V or Ctrl+V), drop one here, or load a file.</p>
          <p className="muted">Compare the model with it side by side; the Hero view matches a
            low front three-quarter photograph.</p>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </aside>
  );
}
