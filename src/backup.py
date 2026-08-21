from pathlib import Path
from datetime import datetime
import shutil

from path_safety import safe_path


def create_backup(source: str | Path) -> Path:
    """Oppretter en sikkerhetskopi av angitt mappe."""

    source_path = safe_path(source)

    if not source_path.exists():
        raise FileNotFoundError(
            f"Backup source not found: {source_path}"
        )

    if not source_path.is_dir():
        raise ValueError(
            f"Backup source must be a directory: {source_path}"
        )

    backup_root = safe_path("_Backups")

    # Backup-mappen skal aldri kunne kopiere seg selv,
    # eller en mappe som inneholder backup-mappen.
    if (
        source_path == backup_root
        or backup_root.is_relative_to(source_path)
    ):
        raise ValueError(
            f"Backup source cannot contain backup destination: {source_path}"
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    backup_path = safe_path(
        f"_Backups/backup_{timestamp}"
    )

    backup_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copytree(
        source_path,
        backup_path
    )

    return backup_path