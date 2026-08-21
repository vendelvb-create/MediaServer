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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

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
