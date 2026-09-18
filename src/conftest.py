import pytest


@pytest.fixture(autouse=True)
def isolated_mediaserver_root(tmp_path, monkeypatch):
    """
    Every test runs against an isolated temporary MediaServer root.

    This is a hard safety barrier: tests never write to the real D:\MediaServer.
    """
    root = tmp_path / "MediaServer"
    root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("MEDIASERVER_ROOT", str(root))
    return root
