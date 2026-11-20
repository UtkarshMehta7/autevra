from pathlib import Path

from fastapi.testclient import TestClient

from autevra.config import Settings
from autevra.desktop import data_dir, free_port
from autevra.main import create_app


def test_data_folder_per_operating_system() -> None:
    home = Path("/home/u")
    assert data_dir("darwin", {}, home) == home / "Library/Application Support/Autevra"
    assert data_dir("win32", {"APPDATA": "C:/Users/u/AppData/Roaming"}, home) == Path(
        "C:/Users/u/AppData/Roaming/Autevra")  # fmt: skip
    assert data_dir("linux", {}, home) == home / ".local/share/autevra"


def test_free_port_is_usable() -> None:
    assert 1024 < free_port() < 65536


def test_backend_serves_the_built_studio(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<html>studio</html>")
    (dist / "assets" / "app.js").write_text("console.log(1)")
    app = create_app(Settings(data_dir=tmp_path / "data", static_dir=dist, llm_provider="off"))
    client = TestClient(app)
    assert client.get("/api/health").json()["status"] == "ok"
    assert client.get("/assets/app.js").text == "console.log(1)"
    assert "studio" in client.get("/studio/abc/aircraft").text  # client-side route
    assert client.get("/api/no-such-route").status_code == 404
    assert "studio" in client.get("/../../etc/passwd").text  # never escapes the folder
