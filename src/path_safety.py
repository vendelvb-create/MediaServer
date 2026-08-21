from pathlib import Path


def get_test_root() -> Path:
    """Returnerer den faste testroten."""
    return (Path.home() / "Desktop" / "MediaLibrary_Test").resolve()


def safe_path(path: str | Path) -> Path:
    """
    Returnerer en sikker absolutt sti innenfor testroten.

    Relative stier tolkes alltid relativt til MediaLibrary_Test,
    ikke relativt til terminalens nåværende arbeidsmappe.
    """
    root = get_test_root()
    candidate = Path(path)

    if not candidate.is_absolute():
        candidate = root / candidate

    candidate = candidate.resolve()

    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"Unsafe path rejected: {candidate}"
        ) from exc

    return candidate
