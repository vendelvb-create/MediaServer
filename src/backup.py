from pathlib import Path
from datetime import datetime
import shutil


def create_backup(source: str | Path) -> Path:
    """Oppretter en sikkerhetskopi av angitt mappe."""

    source_path = Path(source).expanduser().resolve()

    if not source_path.exists():
        raise FileNotFoundError(f"Backup source not found: {source_path}")

    backup_root = (
        Path.home()
        / "Desktop"
        / "Medialibrary_test"
        / "_Backups"
    ).resolve()

    backup_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_root / f"backup_{timestamp}"

    shutil.copytree(source_path, backup_path)

    return backup_path
