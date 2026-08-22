from pathlib import Path
from typing import Callable

from backup import create_backup
from block_state import (
    APPROVED,
    BACKED_UP,
    COMPLETED,
    RUNNING,
    VERIFIED,
    approve_block,
    begin_verification,
    complete_block,
    get_block_state,
    mark_backup_completed,
    start_block,
    verify_block,
)
from logger import BuildLog, log_build_complete, log_build_failure, start_build_log


class BuildWorkflowError(RuntimeError):
    """Feil i kontrollert build-workflow."""


def run_build_workflow(
    block_id: str,
    build_operation: Callable[[], None],
    verification_operation: Callable[[], bool],
    backup_source: str | Path,
    user_approved_start: bool = False,
) -> BuildLog:
    """
    Kjører én kontrollert block-workflow.

    Rekkefølge:
        USER APPROVAL
        -> BUILD
        -> LOG
        -> VERIFY
        -> BACKUP

    APPROVED håndteres separat og krever en eksplisitt
    brukerhandling via approve_completed_block().

    Workflowen starter aldri neste blokk automatisk.

    Denne funksjonen bygger ikke selve mediakatalogen.
    build_operation må eksplisitt leveres av den som kaller workflowen.
    """

    build_log = start_build_log(
        block_id=block_id,
        operation="controlled block build",
    )

    try:
        start_block(
            block_id,
            user_approved=user_approved_start,
        )

        if get_block_state(block_id) != RUNNING:
            raise BuildWorkflowError(
                f"Block {block_id} did not enter RUNNING state."
            )

        build_operation()

        complete_block(block_id)

        if get_block_state(block_id) != COMPLETED:
            raise BuildWorkflowError(
                f"Block {block_id} did not enter COMPLETED state."
            )

        begin_verification(block_id)

        verification_passed = verification_operation()

        if not verification_passed:
            from block_state import fail_block

            fail_block(block_id)

            build_log.set_verification_result("FAILED")
            return _write_failure_log(
                build_log,
                f"Verification failed for block {block_id}.",
            )

        verify_block(block_id)

        if get_block_state(block_id) != VERIFIED:
            raise BuildWorkflowError(
                f"Block {block_id} did not enter VERIFIED state."
            )

        backup_path = create_backup(backup_source)

        if not backup_path.exists():
            raise BuildWorkflowError(
                f"Backup was not created for block {block_id}."
            )

        mark_backup_completed(block_id)

        if get_block_state(block_id) != BACKED_UP:
            raise BuildWorkflowError(
                f"Block {block_id} did not enter BACKED_UP state."
            )

        build_log.set_verification_result("VERIFIED")
        build_log.final_result = "SUCCESS"

        log_build_complete(
            build_log,
            final_result="SUCCESS",
            verification_result="VERIFIED",
        )

        return build_log

    except Exception as exc:
        _fail_block_if_possible(block_id)

        return _write_failure_log(
            build_log,
            f"CRITICAL: {exc}",
        )


def approve_completed_block(block_id: str) -> str:
    """
    Utfører eksplisitt bruker-godkjenning av en ferdig backupet blokk.

    Dette er en separat operasjon med vilje.

    Workflowen godkjenner aldri automatisk en blokk og starter
    aldri neste blokk automatisk.
    """

    current_state = get_block_state(block_id)

    if current_state != BACKED_UP:
        raise BuildWorkflowError(
            f"Block {block_id} cannot be approved from state "
            f"{current_state}. Expected BACKED_UP."
        )

    new_state = approve_block(block_id)

    if new_state != APPROVED:
        raise BuildWorkflowError(
            f"Block {block_id} was not approved correctly."
        )

    return new_state


def _fail_block_if_possible(block_id: str) -> None:
    """
    Forsøker å markere en pågående blokk som FAILED.

    En allerede terminal blokk endres ikke.
    """

    try:
        from block_state import FAILED, VERIFYING, fail_block

        current_state = get_block_state(block_id)

        if current_state in {RUNNING, VERIFYING}:
            fail_block(block_id)

        elif current_state == FAILED:
            return

        elif current_state in {
            COMPLETED,
            VERIFIED,
            BACKED_UP,
            APPROVED,
        }:
            return

    except Exception:
        # Den opprinnelige feilen skal bevares.
        return


def _write_failure_log(
    build_log: BuildLog,
    error: str,
) -> BuildLog:
    """Registrerer og skriver en failure-logg."""

    build_log.fail(error)

    log_build_failure(
        build_log,
        error,
    )

    return build_log