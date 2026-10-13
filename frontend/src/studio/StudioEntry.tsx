import { useEffect, useState } from "react";
import { Navigate, useParams } from "react-router";
import { api, backendHint } from "../api/client";
import { recall } from "./lastProject";

/** /studio and /studio/:id: open a project's design workspace (creating one if none exist). */
export function StudioEntry() {
  const { projectId } = useParams();
  const [target, setTarget] = useState<string | null>(projectId ?? null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    if (projectId) return;
    (async () => {
      try {
        const list = await api.listProjects();
        const last = recall();
        const chosen = list.find((p) => p.id === last) ?? list[0]
          ?? await api.createProject("My first vehicle");
        setTarget(chosen.id);
      } catch (e) {
        setError((e as Error).message);
      }
    })();
  }, [projectId]);
  if (error) return <div className="notice-page"><h1>Backend unreachable</h1><p>{error}. {backendHint()}</p></div>;
  if (!target) return <div className="notice-page"><p>Opening the studio…</p></div>;
  return <Navigate to={`/studio/${target}/design`} replace />;
}
