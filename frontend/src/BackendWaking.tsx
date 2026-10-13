import { useEffect, useState } from "react";
import { onBackendWaking } from "./api/client";

/** Shown while a sleeping hosted backend starts; the request finishes on its own. */
export function BackendWaking() {
  const [waking, setWaking] = useState(false);
  useEffect(() => onBackendWaking(setWaking), []);
  if (!waking) return null;
  return (
    <div className="backend-waking" role="status">
      Starting the engineering backend. The free host sleeps when unused, so this can take a
      minute or two.
    </div>
  );
}
