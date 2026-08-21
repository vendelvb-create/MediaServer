from pathlib import Path


def get_test_root() -> Path:
    """
    Returnerer den godkjente testroten.

    All filskriving i testfasen skal holdes innenfor denne katalogen.
    """
    return (Path.home() / "Desktop" / "MediaLibrary_Test").resolve()


def safe_path(path: str | Path) -> Path:
    """
    Kontrollerer at en sti ligger innenfor den godkjente testroten.

    Avviser blant annet:
    - path traversal med ..
    - absolutte stier utenfor testroten
    - stier til andre kataloger eller disker
    """

    root = get_test_root()
    candidate = Path(path).expanduser().resolve()

    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"Unsafe path rejected: {candidate}"
        ) from exc

    return candidate
