from pathlib import Path
import shutil

import pytest

from backup import create_backup, restore_backup
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
            shutil.rmtree(source)

        if "backup_path" in locals() and backup_path.exists():
            shutil.rmtree(backup_path)


def test_create_backup_rejects_missing_source():
    with pytest.raises(FileNotFoundError):
        create_backup("_Test_Backup_Source_Does_Not_Exist")


def test_create_backup_rejects_file_source():
    root = get_test_root()
    source_file = root / "_Test_Backup_File"

    source_file.write_text(
        "not a directory",
        encoding="utf-8",
    )

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


def test_restore_backup_copies_backup_to_destination():
    root = get_test_root()

    source = root / "_Test_Restore_Source"
    destination = root / "_Test_Restore_Destination"

    source.mkdir(parents=True, exist_ok=True)
    (source / "restore.txt").write_text(
        "restore test",
        encoding="utf-8",
    )

    backup_path = None

    try:
        backup_path = create_backup(source)

        restored_path = restore_backup(
            backup_path,
            destination,
        )

        assert restored_path == destination
        assert restored_path.exists()
        assert restored_path.is_dir()
        assert (
            restored_path / "restore.txt"
        ).read_text(encoding="utf-8") == "restore test"

    finally:
        if source.exists():
            shutil.rmtree(source)

        if destination.exists():
            shutil.rmtree(destination)

        if backup_path is not None and backup_path.exists():
            shutil.rmtree(backup_path)


def test_restore_backup_rejects_missing_backup():
    with pytest.raises(FileNotFoundError):
        restore_backup(
            "_Backups/backup_that_does_not_exist",
            "_Test_Restore_Destination",
        )


def test_restore_backup_rejects_backup_file():
    root = get_test_root()
    backup_root = safe_path("_Backups")

    backup_root.mkdir(parents=True, exist_ok=True)

    backup_file = backup_root / "_Test_Backup_File"
    backup_file.write_text(
        "not a directory",
        encoding="utf-8",
    )

    try:
        with pytest.raises(ValueError):
            restore_backup(
                backup_file,
                "_Test_Restore_Destination",
            )
    finally:
        backup_file.unlink(missing_ok=True)


def test_restore_backup_rejects_backup_root_as_source():
    with pytest.raises(ValueError):
        restore_backup(
            "_Backups",
            "_Test_Restore_Destination",
        )


def test_restore_backup_rejects_source_outside_backup_root():
    root = get_test_root()
    source = root / "_Test_Not_A_Backup"

    source.mkdir(parents=True, exist_ok=True)

    try:
        with pytest.raises(ValueError):
            restore_backup(
                source,
                "_Test_Restore_Destination",
            )
    finally:
        shutil.rmtree(source)


def test_restore_backup_rejects_existing_destination():
    root = get_test_root()

    source = root / "_Test_Restore_Source"
    destination = root / "_Test_Restore_Destination"

    source.mkdir(parents=True, exist_ok=True)
    destination.mkdir(parents=True, exist_ok=True)

    backup_path = None

    try:
        (source / "restore.txt").write_text(
            "restore test",
            encoding="utf-8",
        )

        backup_path = create_backup(source)

        with pytest.raises(FileExistsError):
            restore_backup(
                backup_path,
                destination,
            )

        assert destination.exists()
        assert destination.is_dir()

    finally:
        if source.exists():
            shutil.rmtree(source)

        if destination.exists():
            shutil.rmtree(destination)

        if backup_path is not None and backup_path.exists():
            shutil.rmtree(backup_path)


def test_restore_backup_rejects_backup_destination():
    root = get_test_root()
    source = root / "_Test_Restore_Source"

    source.mkdir(parents=True, exist_ok=True)

    backup_path = None

    try:
        (source / "restore.txt").write_text(
            "restore test",
            encoding="utf-8",
        )

        backup_path = create_backup(source)

        with pytest.raises(ValueError):
            restore_backup(
                backup_path,
                "_Backups/restored",
            )

    finally:
        if source.exists():
            shutil.rmtree(source)

        if backup_path is not None and backup_path.exists():
            shutil.rmtree(backup_path)


def test_restore_backup_preserves_existing_backup():
    root = get_test_root()

    source = root / "_Test_Restore_Source"
    destination = root / "_Test_Restore_Destination"

    source.mkdir(parents=True, exist_ok=True)
    destination.mkdir(parents=True, exist_ok=True)

    backup_path = None

    try:
        (source / "restore.txt").write_text(
            "restore test",
            encoding="utf-8",
        )

        backup_path = create_backup(source)

        with pytest.raises(FileExistsError):
            restore_backup(
                backup_path,
                destination,
            )

        assert backup_path.exists()
        assert backup_path.is_dir()

    finally:
        if source.exists():
            shutil.rmtree(source)

        if destination.exists():
            shutil.rmtree(destination)

        if backup_path is not None and backup_path.exists():
            shutil.rmtree(backup_path)


def test_restore_backup_rejects_absolute_destination_outside_test_root():
    outside_destination = Path.home() / "Desktop" / "_Unsafe_Restore"

    with pytest.raises(ValueError):
        restore_backup(
            "_Backups/backup_example",
            outside_destination,
        )


def test_restore_backup_rejects_parent_traversal_destination():
    with pytest.raises(ValueError):
        restore_backup(
            "_Backups/backup_example",
            "../_Unsafe_Restore",
        )