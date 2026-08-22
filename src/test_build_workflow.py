from pathlib import Path
import shutil

import pytest

from backup import create_backup
from block_state import (
    APPROVED,
    BACKED_UP,
    FAILED,
    RUNNING,
    VERIFIED,
    get_block_state,
    save_state,
)
from build_workflow import (
    BuildWorkflowError,
    approve_completed_block,
    run_build_workflow,
)
from path_safety import get_test_root, safe_path


def _cleanup_path(path: Path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def _reset_state() -> None:
    state_file = safe_path("_Data/block_state.json")
    state_file.unlink(missing_ok=True)


def _create_backup_source(name: str) -> Path:
    source = get_test_root() / name
    _cleanup_path(source)

    source.mkdir(parents=True, exist_ok=True)
    (source / "build.txt").write_text(
        "workflow test",
        encoding="utf-8",
    )

    return source


def test_workflow_requires_explicit_user_approval():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    build_called = False

    def build_operation() -> None:
        nonlocal build_called
        build_called = True

    def verification_operation() -> bool:
        return True

    try:
        log = run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=False,
        )

        assert build_called is False
        assert log.final_result == "FAILED"
        assert get_block_state("0001-1000") == "NOT_STARTED"

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_runs_build_after_explicit_user_approval():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    build_called = False

    def build_operation() -> None:
        nonlocal build_called
        build_called = True

    def verification_operation() -> bool:
        return True

    try:
        log = run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert build_called is True
        assert log.final_result == "SUCCESS"
        assert log.verification_result == "VERIFIED"
        assert get_block_state("0001-1000") == "BACKED_UP"

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_fails_when_build_operation_raises():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    def build_operation() -> None:
        raise RuntimeError("Build failed.")

    def verification_operation() -> bool:
        return True

    try:
        log = run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert log.final_result == "FAILED"
        assert "CRITICAL: Build failed." in log.errors
        assert get_block_state("0001-1000") == FAILED

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_fails_when_verification_returns_false():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    def build_operation() -> None:
        return None

    def verification_operation() -> bool:
        return False

    try:
        log = run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert log.final_result == "FAILED"
        assert log.verification_result == "FAILED"
        assert get_block_state("0001-1000") == FAILED

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_creates_backup_after_successful_verification():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")
    backup_root = safe_path("_Backups")

    try:
        existing_backups = set(backup_root.glob("backup_*"))

        def build_operation() -> None:
            return None

        def verification_operation() -> bool:
            return True

        log = run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        new_backups = set(backup_root.glob("backup_*")) - existing_backups

        assert log.final_result == "SUCCESS"
        assert len(new_backups) == 1

        backup_path = next(iter(new_backups))

        try:
            assert backup_path.is_dir()
            assert (
                backup_path / "build.txt"
            ).read_text(encoding="utf-8") == "workflow test"
        finally:
            _cleanup_path(backup_path)

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_does_not_approve_block_automatically():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    try:
        def build_operation() -> None:
            return None

        def verification_operation() -> bool:
            return True

        run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert get_block_state("0001-1000") == BACKED_UP
        assert get_block_state("0001-1000") != APPROVED

    finally:
        _cleanup_path(source)
        _reset_state()


def test_user_can_explicitly_approve_backed_up_block():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    try:
        def build_operation() -> None:
            return None

        def verification_operation() -> bool:
            return True

        run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert get_block_state("0001-1000") == BACKED_UP

        result = approve_completed_block("0001-1000")

        assert result == APPROVED
        assert get_block_state("0001-1000") == APPROVED

    finally:
        _cleanup_path(source)
        _reset_state()


def test_next_block_cannot_start_until_previous_block_is_approved():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    try:
        def build_operation() -> None:
            return None

        def verification_operation() -> bool:
            return True

        run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert get_block_state("0001-1000") == BACKED_UP

        with pytest.raises(BuildWorkflowError):
            approve_completed_block("1001-2000")

    finally:
        _cleanup_path(source)
        _reset_state()


def test_approved_previous_block_allows_next_block_start():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    try:
        def build_operation() -> None:
            return None

        def verification_operation() -> bool:
            return True

        run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert get_block_state("0001-1000") == BACKED_UP

        assert (
            approve_completed_block("0001-1000")
            == APPROVED
        )

        assert get_block_state("0001-1000") == APPROVED

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_does_not_start_next_block_automatically():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    try:
        def build_operation() -> None:
            return None

        def verification_operation() -> bool:
            return True

        run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert get_block_state("0001-1000") == BACKED_UP
        assert get_block_state("1001-2000") == "NOT_STARTED"

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_failure_does_not_create_successful_backup_state():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    def build_operation() -> None:
        raise RuntimeError("Critical build failure.")

    def verification_operation() -> bool:
        return True

    try:
        log = run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert log.final_result == "FAILED"
        assert get_block_state("0001-1000") == FAILED
        assert get_block_state("0001-1000") != BACKED_UP

    finally:
        _cleanup_path(source)
        _reset_state()


def test_workflow_does_not_verify_when_verification_fails():
    _reset_state()

    source = _create_backup_source("_Test_Workflow_Source")

    try:
        def build_operation() -> None:
            return None

        def verification_operation() -> bool:
            return False

        run_build_workflow(
            block_id="0001-1000",
            build_operation=build_operation,
            verification_operation=verification_operation,
            backup_source=source,
            user_approved_start=True,
        )

        assert get_block_state("0001-1000") == FAILED
        assert get_block_state("0001-1000") != VERIFIED

    finally:
        _cleanup_path(source)
        _reset_state()


def test_approve_completed_block_rejects_wrong_state():
    _reset_state()

    save_state(
        {
            "blocks": {
                "0001-1000": {
                    "state": RUNNING,
                }
            }
        }
    )

    try:
        with pytest.raises(BuildWorkflowError):
            approve_completed_block("0001-1000")
    finally:
        _reset_state()