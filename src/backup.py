from datetime import datetime
from pathlib import Path
import shutil

from path_safety import safe_path


def create_backup(source: str | Path) -> Path:
    """Oppretter en datert sikkerhetskopi av en katalog."""

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

    backup_path = backup_root / f"backup_{timestamp}"

    backup_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copytree(
        source_path,
        backup_path,
    )

    return backup_path


def restore_backup(
    backup: str | Path,
    destination: str | Path,
) -> Path:
    """
    Gjenoppretter en backup til en eksplisitt angitt destination.

    Restore er konservativ:
    - backup må ligge under _Backups/
    - destination må ligge under testroten
    - _Backups kan ikke brukes som destination
    - eksisterende destination avvises
    - ingen eksisterende eller ukjente filer slettes automatisk
    """

    backup_path = safe_path(backup)
    destination_path = safe_path(destination)

    backup_root = safe_path("_Backups")

    if not backup_path.exists():
        raise FileNotFoundError(
            f"Backup not found: {backup_path}"
        )

    if not backup_path.is_dir():
        raise ValueError(
            f"Backup source must be a directory: {backup_path}"
        )

    if not backup_path.is_relative_to(backup_root):
        raise ValueError(
            f"Restore source must be inside backup root: {backup_path}"
        )

    if backup_path == backup_root:
        raise ValueError(
            "Restore source cannot be the backup root"
        )

    if destination_path == backup_root:
        raise ValueError(
            "Restore destination cannot be the backup root"
        )

    if destination_path.is_relative_to(backup_root):
        raise ValueError(
            f"Restore destination cannot be inside backup root: "
            f"{destination_path}"
        )

    if destination_path.exists():
        raise FileExistsError(
            f"Restore destination already exists: {destination_path}"
        )

    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copytree(
        backup_path,
        destination_path,
    )

    return destination_path