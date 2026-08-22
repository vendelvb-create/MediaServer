import json

import pytest

from block_state import (
    APPROVED,
    BACKED_UP,
    COMPLETED,
    FAILED,
    NOT_STARTED,
    RUNNING,
    VERIFIED,
    VERIFYING,
    approve_block,
    begin_verification,
    can_start_block,
    complete_block,
    fail_block,
    get_block_state,
    get_state_file,
    load_state,
    mark_backup_completed,
    save_state,
    start_block,
    transition_block,
)
from path_safety import get_test_root


@pytest.fixture(autouse=True)
def clean_state_file():
    state_file = get_state_file()

    if state_file.exists():
        state_file.unlink()

    yield

    if state_file.exists():
        state_file.unlink()


def test_get_state_file_is_inside_test_root():
    state_file = get_state_file()

    assert state_file.resolve().is_relative_to(
        get_test_root().resolve()
    )
    assert state_file.name == "block_state.json"


def test_load_state_returns_empty_dict_when_missing():
    state_file = get_state_file()

    if state_file.exists():
        state_file.unlink()

    assert load_state() == {}


def test_save_and_load_state():
    state = {
        "block": "0001-1000",
        "status": "complete",
    }

    save_state(state)

    assert get_state_file().exists()
    assert load_state() == state


def test_save_state_creates_parent_directory():
    state_file = get_state_file()

    if state_file.exists():
        state_file.unlink()

    if state_file.parent.exists():
        import shutil
        shutil.rmtree(state_file.parent)

    save_state({"test": True})

    assert state_file.exists()
    assert json.loads(
        state_file.read_text(encoding="utf-8")
    ) == {"test": True}


def test_new_block_defaults_to_not_started():
    assert get_block_state("0001-1000") == NOT_STARTED


def test_first_block_requires_explicit_user_approval():
    assert can_start_block(
        "0001-1000",
        user_approved=False,
    ) is False

    with pytest.raises(ValueError):
        start_block(
            "0001-1000",
            user_approved=False,
        )

    assert get_block_state("0001-1000") == NOT_STARTED


def test_first_block_can_start_with_explicit_user_approval():
    assert can_start_block(
        "0001-1000",
        user_approved=True,
    ) is True

    assert start_block(
        "0001-1000",
        user_approved=True,
    ) == RUNNING

    assert get_block_state("0001-1000") == RUNNING


def test_block_follows_required_state_sequence():
    block_id = "0001-1000"

    assert start_block(
        block_id,
        user_approved=True,
    ) == RUNNING

    assert complete_block(block_id) == COMPLETED
    assert begin_verification(block_id) == VERIFYING
    assert transition_block(
        block_id,
        VERIFIED,
    ) == VERIFIED
    assert mark_backup_completed(block_id) == BACKED_UP
    assert approve_block(block_id) == APPROVED

    assert get_block_state(block_id) == APPROVED


def test_invalid_state_transition_is_rejected():
    block_id = "0001-1000"

    with pytest.raises(ValueError):
        transition_block(
            block_id,
            VERIFIED,
        )

    assert get_block_state(block_id) == NOT_STARTED


def test_failed_block_cannot_continue():
    block_id = "0001-1000"

    start_block(
        block_id,
        user_approved=True,
    )

    assert fail_block(block_id) == FAILED
    assert get_block_state(block_id) == FAILED

    with pytest.raises(ValueError):
        complete_block(block_id)

    assert get_block_state(block_id) == FAILED


def test_next_block_cannot_start_before_previous_block_is_approved():
    first_block = "0001-1000"
    second_block = "1001-2000"

    start_block(
        first_block,
        user_approved=True,
    )

    assert can_start_block(
        second_block,
        user_approved=True,
    ) is False

    with pytest.raises(ValueError):
        start_block(
            second_block,
            user_approved=True,
        )

    assert get_block_state(second_block) == NOT_STARTED


def test_next_block_can_start_after_previous_block_is_approved():
    first_block = "0001-1000"
    second_block = "1001-2000"

    start_block(
        first_block,
        user_approved=True,
    )
    complete_block(first_block)
    begin_verification(first_block)
    transition_block(first_block, VERIFIED)
    mark_backup_completed(first_block)
    approve_block(first_block)

    assert get_block_state(first_block) == APPROVED

    assert can_start_block(
        second_block,
        user_approved=True,
    ) is True

    assert start_block(
        second_block,
        user_approved=True,
    ) == RUNNING

    assert get_block_state(second_block) == RUNNING


def test_user_approval_alone_cannot_bypass_previous_block():
    second_block = "1001-2000"

    assert can_start_block(
        second_block,
        user_approved=True,
    ) is False

    with pytest.raises(ValueError):
        start_block(
            second_block,
            user_approved=True,
        )

    assert get_block_state(second_block) == NOT_STARTED


def test_invalid_block_id_is_rejected():
    with pytest.raises(ValueError):
        can_start_block(
            "not-a-block",
            user_approved=True,
        )

    with pytest.raises(ValueError):
        can_start_block(
            "1001-1999",
            user_approved=True,
        )


def test_corrupt_state_json_is_rejected():
    state_file = get_state_file()
    state_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    state_file.write_text(
        "{ this is not valid json",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_state()


def test_non_object_state_json_is_rejected():
    state_file = get_state_file()
    state_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    state_file.write_text(
        '["not", "an", "object"]',
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_state()


def test_invalid_state_value_is_rejected():
    save_state(
        {
            "blocks": {
                "0001-1000": {
                    "state": "INVALID_STATE",
                }
            }
        }
    )

    with pytest.raises(ValueError):
        get_block_state("0001-1000")


def test_same_state_transition_is_rejected():
    block_id = "0001-1000"

    start_block(
        block_id,
        user_approved=True,
    )

    with pytest.raises(ValueError):
        transition_block(
            block_id,
            RUNNING,
        )

    assert get_block_state(block_id) == RUNNING


def test_approved_block_cannot_be_started_again():
    block_id = "0001-1000"

    start_block(
        block_id,
        user_approved=True,
    )
    complete_block(block_id)
    begin_verification(block_id)
    transition_block(block_id, VERIFIED)
    mark_backup_completed(block_id)
    approve_block(block_id)

    assert get_block_state(block_id) == APPROVED

    with pytest.raises(ValueError):
        start_block(
            block_id,
            user_approved=True,
        )


def test_save_state_is_atomic_and_leaves_no_tmp():
    """Normal atomic save must leave a valid JSON file and no leftover .tmp."""
    state = {
        "blocks": {
            "0001-1000": {
                "state": RUNNING,
            }
        }
    }

    save_state(state)

    state_file = get_state_file()
    tmp_file = state_file.with_name(state_file.name + ".tmp")

    assert state_file.exists()
    assert not tmp_file.exists()
    assert load_state() == state
    # Ensure the file content is valid JSON
    assert json.loads(state_file.read_text(encoding="utf-8")) == state


def test_failed_write_does_not_destroy_previous_state(monkeypatch):
    """
    If writing the new state fails, the previous valid state file
    must remain intact and loadable.
    """
    original = {
        "blocks": {
            "0001-1000": {
                "state": COMPLETED,
            }
        }
    }
    save_state(original)

    state_file = get_state_file()
    assert load_state() == original

    def failing_dump(*args, **kwargs):
        raise OSError("Simulated write failure during json.dump")

    monkeypatch.setattr(json, "dump", failing_dump)

    with pytest.raises(OSError):
        save_state(
            {
                "blocks": {
                    "0001-1000": {
                        "state": FAILED,
                    }
                }
            }
        )

    # Previous valid state must still be present and unchanged.
    assert state_file.exists()
    assert load_state() == original

    tmp_file = state_file.with_name(state_file.name + ".tmp")
    # Temporary file should have been cleaned up on failure.
    assert not tmp_file.exists()
