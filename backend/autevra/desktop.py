"""Desktop entry point: the whole application as one local process.

``python -m autevra.desktop --static <frontend/dist>`` starts the backend on 127.0.0.1 at a
free port, serving the built studio and the API from the same origin, with the design data
in the operating system's per-user application folder. A native shell (planned: Tauri, with
this process bundled as its sidecar by PyInstaller, on macOS and Windows) reads the
``AUTEVRA_READY <url>`` line from stdout and opens a window on that URL.

Nothing here is platform-specific beyond choosing the data folder.
"""

import argparse
import os
import socket
import sys
from pathlib import Path

APP = "Autevra"


def data_dir(platform: str = sys.platform, env: dict[str, str] | None = None,
             home: Path | None = None) -> Path:  # fmt: skip
    """The per-user application data folder on this operating system."""
    env = dict(os.environ) if env is None else env
    home = Path.home() if home is None else home
    if platform == "darwin":
        return home / "Library" / "Application Support" / APP
    if platform.startswith("win"):
        base = env.get("APPDATA") or str(home / "AppData" / "Roaming")
        return Path(base) / APP
    base = env.get("XDG_DATA_HOME") or str(home / ".local" / "share")
    return Path(base) / APP.lower()


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="autevra-desktop")
    parser.add_argument("--static", type=Path, required=True, help="built studio folder")
    parser.add_argument("--port", type=int, default=0, help="0 picks a free port")
    parser.add_argument("--data", type=Path, default=None, help="design data folder")
    args = parser.parse_args(argv)

    import uvicorn

    from autevra.config import Settings
    from autevra.main import create_app

    port = args.port or free_port()
    origin = f"http://127.0.0.1:{port}"
    settings = Settings(data_dir=args.data or data_dir(), static_dir=args.static,
                        cors_origins=[origin])  # fmt: skip
    app = create_app(settings)
    print(f"AUTEVRA_READY {origin}", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


if __name__ == "__main__":
    main()
