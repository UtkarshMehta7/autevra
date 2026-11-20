import { useRef } from "react";

/**
 * A drag handle between two panels. ``onDrag`` receives the pointer travel since the drag
 * started (x for a vertical handle, y for a horizontal one); arrow keys move it by 16 px
 * (64 px with Shift) and a double click runs ``onReset``.
 */
export function Splitter({ orientation, label, onStart, onDrag, onReset, area }: {
  orientation: "vertical" | "horizontal";
  label: string;
  area: string;
  onStart: () => void;
  onDrag: (delta: number) => void;
  onReset: () => void;
}) {
  const origin = useRef<number | null>(null);
  const vertical = orientation === "vertical";
  return (
    <div
      className={`splitter ${orientation}`}
      style={{ gridArea: area }}
      role="separator"
      aria-orientation={orientation}
      aria-label={label}
      title={`${label}: drag to resize, double-click to reset`}
      tabIndex={0}
      onPointerDown={(e) => {
        e.preventDefault();
        origin.current = vertical ? e.clientX : e.clientY;
        onStart();
        e.currentTarget.setPointerCapture(e.pointerId);
        document.body.classList.add(vertical ? "resizing-x" : "resizing-y");
      }}
      onPointerMove={(e) => {
        if (origin.current === null) return;
        onDrag((vertical ? e.clientX : e.clientY) - origin.current);
      }}
      onPointerUp={() => {
        origin.current = null;
        document.body.classList.remove("resizing-x", "resizing-y");
      }}
      onDoubleClick={onReset}
      onKeyDown={(e) => {
        const step = e.shiftKey ? 64 : 16;
        const keys = vertical ? ["ArrowLeft", "ArrowRight"] : ["ArrowUp", "ArrowDown"];
        const i = keys.indexOf(e.key);
        if (i < 0) return;
        e.preventDefault();
        onStart();
        onDrag(i === 0 ? -step : step);
      }}
    />
  );
}
