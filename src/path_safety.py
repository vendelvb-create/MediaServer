from __future__ import annotations

import os
from pathlib import Path


ENV_ROOT = "MEDIASERVER_ROOT"
WINDOWS_DEFAULT_ROOT = Path(r"D:\MediaServer")


def get_media_root() -> Path:
    """
    Return the active MediaServer root.

    Production on Windows defaults to D:\MediaServer.
    Tests and non-Windows environments MUST set MEDIASERVER_ROOT explicitly.
    """
    configured = os.environ.get(ENV_ROOT)

    if configured:
        return Path(configured).expanduser().resolve()

    if os.name != "nt":
        raise RuntimeError(
            f"{ENV_ROOT} must be set outside Windows. "
            "Refusing to guess a writable MediaServer root."
        )

    return WINDOWS_DEFAULT_ROOT.resolve()


def get_test_root() -> Path:
    """
    Backwards-compatible alias.

    New code should use get_media_root(). Tests override MEDIASERVER_ROOT
    to an isolated temporary directory.
    """
    return get_media_root()


def safe_path(path: str | Path) -> Path:
    """
    Resolve a path and guarantee it stays inside the active MediaServer root.

    Relative paths are always interpreted relative to the configured root,
    never relative to the process working directory.
    """
    root = get_media_root()
    candidate = Path(path)

    if not candidate.is_absolute():
        candidate = root / candidate

    candidate = candidate.resolve()

    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Unsafe path rejected: {candidate}") from exc

    return candidate
