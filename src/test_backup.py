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


def test_create_backup_cleans_partial_on_failure():
    """A failed backup must not leave a final-named backup_* directory."""
    from unittest.mock import patch

    root = get_test_root()
    source = root / "_Test_Backup_Fail_Source"
    source.mkdir(parents=True, exist_ok=True)
    (source / "data.txt").write_text("data", encoding="utf-8")

    backup_root = safe_path("_Backups")
    before_backups = set(backup_root.glob("backup_*"))
    before_tmps = set(backup_root.glob(".tmp_backup_*"))

    try:
        with patch("backup.shutil.copytree", side_effect=OSError("simulated interrupt")):
            with pytest.raises(OSError, match="simulated interrupt"):
                create_backup(source)

        after_backups = set(backup_root.glob("backup_*"))
        after_tmps = set(backup_root.glob(".tmp_backup_*"))

        # No new final-named backup must appear
        assert after_backups == before_backups
        # Temporary work directory must be cleaned up
        assert after_tmps == before_tmps

    finally:
        if source.exists():
            shutil.rmtree(source)
        # Safety cleanup of any leftover tmp from a broken implementation
        for p in backup_root.glob(".tmp_backup_*"):
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)


def test_create_backup_atomic_success_leaves_only_final_name():
    """Successful backup appears only under the final backup_* name."""
    root = get_test_root()
    source = root / "_Test_Backup_Atomic_Source"
    source.mkdir(parents=True, exist_ok=True)
    (source / "ok.txt").write_text("ok", encoding="utf-8")

    backup_root = safe_path("_Backups")
    before_tmps = set(backup_root.glob(".tmp_backup_*"))

    backup_path = None
    try:
        backup_path = create_backup(source)

        assert backup_path.exists()
        assert backup_path.is_dir()
        assert backup_path.name.startswith("backup_")
        assert (backup_path / "ok.txt").read_text(encoding="utf-8") == "ok"

        # No temporary names left behind after success
        after_tmps = set(backup_root.glob(".tmp_backup_*"))
        assert after_tmps == before_tmps

    finally:
        if source.exists():
            shutil.rmtree(source)
        if backup_path is not None and backup_path.exists():
            shutil.rmtree(backup_path)


def test_create_backup_preserves_existing_valid_backup_on_failure():
    """A failure during a new backup must not destroy previous valid backups."""
    from unittest.mock import patch

    root = get_test_root()
    source = root / "_Test_Backup_Preserve_Source"
    source.mkdir(parents=True, exist_ok=True)
    (source / "data.txt").write_text("data", encoding="utf-8")

    # Create one valid backup first
    existing_backup = create_backup(source)
    assert existing_backup.exists()

    backup_root = safe_path("_Backups")
    before = set(backup_root.glob("backup_*"))

    try:
        with patch("backup.shutil.copytree", side_effect=OSError("disk full")):
            with pytest.raises(OSError):
                create_backup(source)

        after = set(backup_root.glob("backup_*"))
        assert existing_backup in after
        assert after == before
        assert existing_backup.exists()
        assert (existing_backup / "data.txt").read_text(encoding="utf-8") == "data"

    finally:
        if source.exists():
            shutil.rmtree(source)
        if existing_backup.exists():
            shutil.rmtree(existing_backup)
        for p in backup_root.glob(".tmp_backup_*"):
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
