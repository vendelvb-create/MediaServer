from pathlib import Path

import pytest

from backup import create_backup
from path_safety import get_test_root


def test_create_backup_creates_backup():
    root = get_test_root()
    source = root / "Movies"

    source.mkdir(parents=True, exist_ok=True)
    (source / "test.txt").write_text("backup test", encoding="utf-8")

    backup_path = create_backup(source)

    assert backup_path.exists()
    assert backup_path.is_dir()
    assert (backup_path / "test.txt").read_text(encoding="utf-8") == "backup test"


def test_create_backup_rejects_missing_source():
    root = get_test_root()
    missing = root / "DoesNotExist"

    with pytest.raises(FileNotFoundError):
        create_backup(missing)


def test_create_backup_rejects_file_source():
    root = get_test_root()
    source = root / "test_file.txt"

    source.write_text("not a directory", encoding="utf-8")

    with pytest.raises(ValueError):
        create_backup(source)