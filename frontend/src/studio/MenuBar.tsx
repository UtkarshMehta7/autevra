import { useEffect, useRef, useState } from "react";
import { download } from "../api/client";

export interface MenuItem {
  label: string;
  shortcut?: string;
  checked?: boolean;
  disabled?: boolean;
  action?: () => void;
  separator?: boolean;
}

export interface Menu {
  label: string;
  items: MenuItem[];
}

/** A desktop-style menu bar: click a title to open its menu, hover to move between
 * open menus, Escape or a click elsewhere to close. */
export function MenuBar({ menus }: { menus: Menu[] }) {
  const [open, setOpen] = useState<string | null>(null);
  const bar = useRef<HTMLElement>(null);
  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent | KeyboardEvent) => {
      if (e instanceof KeyboardEvent ? e.key === "Escape" : !bar.current?.contains(e.target as Node)) setOpen(null);
    };
    window.addEventListener("mousedown", close);
    window.addEventListener("keydown", close);
    return () => { window.removeEventListener("mousedown", close); window.removeEventListener("keydown", close); };
  }, [open]);
  return (
    <nav className="menubar" ref={bar} aria-label="Menu bar">
      {menus.map((m) => (
        <div key={m.label} className="menu">
          <button className={open === m.label ? "on" : ""} aria-haspopup="menu" aria-expanded={open === m.label}
            onClick={() => setOpen(open === m.label ? null : m.label)}
            onMouseEnter={() => open && setOpen(m.label)}>{m.label}</button>
          {open === m.label && (
            <ul role="menu">
              {m.items.map((item, i) => item.separator ? <li key={i} className="sep" role="separator" /> : (
                <li key={item.label} role="none">
                  <button role={item.checked === undefined ? "menuitem" : "menuitemcheckbox"}
                    aria-checked={item.checked} disabled={item.disabled}
                    onClick={() => { setOpen(null); item.action?.(); }}>
                    <span className="check">{item.checked ? "✓" : ""}</span>
                    <span className="label">{item.label}</span>
                    {item.shortcut && <span className="shortcut">{item.shortcut}</span>}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </nav>
  );
}

/** A menu action that downloads an API file (errors are reported with an alert-free
 * console message; the download link elsewhere shows them inline). */
export function downloadAction(href: string): () => void {
  return () => { download(href).catch((err: Error) => console.error(`download failed: ${err.message}`)); };
}
