import pytest

from autevra.config import Settings, normalise_database_url


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("postgres://u:p@host/db", "postgresql+psycopg://u:p@host/db"),
        (
            "postgresql://u:p@ep-x.neon.tech/db?sslmode=require",
            "postgresql+psycopg://u:p@ep-x.neon.tech/db?sslmode=require",
        ),
        ("postgresql+psycopg://u@h/db", "postgresql+psycopg://u@h/db"),
        ("sqlite:///x.db", "sqlite:///x.db"),
    ],
)
def test_database_urls_name_the_psycopg_driver(given: str, expected: str) -> None:
    assert normalise_database_url(given) == expected


def test_default_database_is_sqlite_in_the_data_dir(tmp_path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.delenv("AUTEVRA_DATABASE_URL", raising=False)
    url = Settings(data_dir=tmp_path).resolved_database_url()
    assert url == f"sqlite:///{(tmp_path / 'autevra.db').resolve()}"


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ('["https://a.netlify.app"]', ["https://a.netlify.app"]),
        ("https://a.netlify.app/", ["https://a.netlify.app"]),
        (
            "https://a.netlify.app, https://b.example",
            ["https://a.netlify.app", "https://b.example"],
        ),
        ("", []),
        ("[]", []),
    ],
)
def test_cors_origins_accept_json_comma_list_or_one_url(given, expected, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("AUTEVRA_CORS_ORIGINS", given)
    assert Settings().cors_origins == expected
