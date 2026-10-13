const LAST_PROJECT = "autevra.lastProject";

export function remember(id: string) {
  try { localStorage.setItem(LAST_PROJECT, id); } catch { /* storage unavailable */ }
}

export function recall(): string | null {
  try { return localStorage.getItem(LAST_PROJECT); } catch { return null; }
}
