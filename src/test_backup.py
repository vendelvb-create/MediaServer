from pathlib import Path

import pytest

from backup import create_backup
from path_safety import get_test_root, safe_path


def test_create_backup_copies_directory():
    root = get_test_root()
    source = root / "_Test_Backup_Source"

    source.mkdir(parents=True, exist_ok=True)
    test_file = source / "test.txt"
    test_file.write_text("backup test", encoding="utf-8")

    backup_root = safe_path("_Backups")
    existing = set(backup_root.glob("backup_*"))

    try:
        backup_path = create_backup(source)

        assert backup_path.exists()
        assert backup_path.is_dir()
        assert backup_path not in existing
        assert (backup_path / "test.txt").read_text(
            encoding="utf-8"
        ) == "backup test"

    finally:
        if source.exists():
            import shutil
            shutil.rmtree(source)

        if "backup_path" in locals() and backup_path.exists():
            import shutil
            shutil.rmtree(backup_path)


def test_create_backup_rejects_missing_source():
    with pytest.raises(FileNotFoundError):
        create_backup("_Test_Backup_Source_Does_Not_Exist")


def test_create_backup_rejects_file_source():
    root = get_test_root()
    source_file = root / "_Test_Backup_File"

    source_file.write_text("not a directory", encoding="utf-8")

    try:
        with pytest.raises(ValueError):
            create_backup(source_file)
    finally:
        source_file.unlink(missing_ok=True)


def test_create_backup_rejects_backup_root_as_source():
    with pytest.raises(ValueError):
        create_backup("_Backups")


def test_create_backup_rejects_test_root_as_source():
    root = get_test_root()

    with pytest.raises(ValueError):
        create_backup(root)
