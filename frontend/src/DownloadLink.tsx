import { type ReactNode, useState } from "react";
import { download } from "./api/client";

/** A link to an API file that downloads it with the visitor's workspace header. */
export function DownloadLink({ href, className, children }: {
  href: string; className?: string; children: ReactNode;
}) {
  const [error, setError] = useState("");
  return (
    <>
      <a className={className} href={href} onClick={(e) => {
        e.preventDefault();
        setError("");
        download(href).catch((err: Error) => setError(err.message));
      }}>{children}</a>
      {error && <span className="bad-text" role="alert"> {error}</span>}
    </>
  );
}
