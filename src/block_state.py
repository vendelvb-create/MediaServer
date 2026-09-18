from pathlib import Path
import json
import os

from path_safety import safe_path


NOT_STARTED = "NOT_STARTED"
RUNNING = "RUNNING"
FAILED = "FAILED"
COMPLETED = "COMPLETED"
VERIFYING = "VERIFYING"
VERIFIED = "VERIFIED"
BACKED_UP = "BACKED_UP"
APPROVED = "APPROVED"

BATCH_SIZE = 500

BLOCK_STATES = {
    NOT_STARTED,
    RUNNING,
    FAILED,
    COMPLETED,
    VERIFYING,
    VERIFIED,
    BACKED_UP,
    APPROVED,
}

STATE_TRANSITIONS = {
    NOT_STARTED: {RUNNING},
    RUNNING: {FAILED, COMPLETED},
    COMPLETED: {VERIFYING},
    VERIFYING: {FAILED, VERIFIED},
    VERIFIED: {BACKED_UP},
    BACKED_UP: {APPROVED},
    FAILED: set(),
    APPROVED: set(),
}


def get_state_file() -> Path:
    """Return the safe persistent batch-state file."""
    return safe_path("Data/block_state.json")


def load_state() -> dict:
    """Load batch state. Missing state is treated as an empty state."""
    state_file = get_state_file()

    if not state_file.exists():
        return {}

    try:
        with state_file.open("r", encoding="utf-8") as file:
            state = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Block state file contains invalid JSON: {state_file}"
        ) from exc

    if not isinstance(state, dict):
        raise ValueError(
            f"Block state must contain a JSON object: {state_file}"
        )

    return state


def save_state(state: dict) -> None:
    """Persist batch state atomically."""
    if not isinstance(state, dict):
        raise ValueError("Block state must be a dictionary.")

    state_file = get_state_file()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = state_file.with_name(state_file.name + ".tmp")

    try:
        with tmp_file.open("w", encoding="utf-8") as file:
            json.dump(state, file, indent=2, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())

        tmp_file.replace(state_file)
    except Exception:
        if tmp_file.exists():
            try:
                tmp_file.unlink()
            except OSError:
                pass
        raise


def _get_blocks(state: dict) -> dict:
    blocks = state.get("blocks", {})

    if not isinstance(blocks, dict):
        raise ValueError("Block state 'blocks' must be a dictionary.")

    return blocks


def _get_block_entry(state: dict, block_id: str) -> dict:
    if not isinstance(block_id, str) or not block_id.strip():
        raise ValueError("block_id must be a non-empty string.")

    blocks = _get_blocks(state)
    entry = blocks.get(block_id)

    if entry is None:
        return {"state": NOT_STARTED}

    if not isinstance(entry, dict):
        raise ValueError(
            f"State for block {block_id} must be a dictionary."
        )

    block_state = entry.get("state", NOT_STARTED)

    if block_state not in BLOCK_STATES:
        raise ValueError(
            f"Invalid state for block {block_id}: {block_state}"
        )

    return entry


def get_block_state(block_id: str) -> str:
    state = load_state()
    return _get_block_entry(state, block_id)["state"]


def _save_block_state(state: dict, block_id: str, new_state: str) -> None:
    if new_state not in BLOCK_STATES:
        raise ValueError(f"Invalid block state: {new_state}")

    blocks = _get_blocks(state)
    entry = blocks.get(block_id, {})

    if not isinstance(entry, dict):
        raise ValueError(
            f"State for block {block_id} must be a dictionary."
        )

    entry["state"] = new_state
    blocks[block_id] = entry
    state["blocks"] = blocks
    save_state(state)


def transition_block(block_id: str, new_state: str) -> str:
    if not isinstance(block_id, str) or not block_id.strip():
        raise ValueError("block_id must be a non-empty string.")

    if new_state not in BLOCK_STATES:
        raise ValueError(f"Invalid block state: {new_state}")

    state = load_state()
    current_state = _get_block_entry(state, block_id)["state"]

    if new_state == current_state:
        raise ValueError(
            f"Block {block_id} is already in state {current_state}."
        )

    if new_state not in STATE_TRANSITIONS[current_state]:
        raise ValueError(
            f"Invalid state transition for block {block_id}: "
            f"{current_state} -> {new_state}"
        )

    _save_block_state(state, block_id, new_state)
    return new_state


def _parse_block_id(block_id: str) -> tuple[int, int]:
    if not isinstance(block_id, str):
        raise ValueError("block_id must be a string.")

    parts = block_id.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid block id format: {block_id}")

    try:
        start = int(parts[0])
        end = int(parts[1])
    except ValueError as exc:
        raise ValueError(f"Invalid block id format: {block_id}") from exc

    if start < 1 or end < start:
        raise ValueError(f"Invalid block range: {block_id}")

    if end - start + 1 != BATCH_SIZE:
        raise ValueError(
            f"Block must contain exactly {BATCH_SIZE} positions: {block_id}"
        )

    if (start - 1) % BATCH_SIZE != 0:
        raise ValueError(
            f"Block start must align to {BATCH_SIZE}-position boundaries: "
            f"{block_id}"
        )

    return start, end


def _previous_block_id(block_id: str) -> str | None:
    """
    Return the previous 500-position batch.

    Examples:
    0001-0500 -> None
    0501-1000 -> 0001-0500
    1001-1500 -> 0501-1000
    """
    start, _ = _parse_block_id(block_id)

    if start == 1:
        return None

    previous_start = start - BATCH_SIZE
    previous_end = start - 1
    return f"{previous_start:04d}-{previous_end:04d}"


def can_start_block(block_id: str, user_approved: bool = False) -> bool:
    if not user_approved:
        return False

    # Validate the identifier even when no state exists yet.
    previous_block = _previous_block_id(block_id)

    if get_block_state(block_id) != NOT_STARTED:
        return False

    if previous_block is None:
        return True

    state = load_state()
    previous_state = _get_block_entry(state, previous_block)["state"]
    return previous_state == APPROVED


def start_block(block_id: str, user_approved: bool = False) -> str:
    if not can_start_block(block_id, user_approved=user_approved):
        raise ValueError(
            f"Block {block_id} cannot be started. "
            "The block must be NOT_STARTED, the user must explicitly "
            "approve the start, and the previous block must be APPROVED."
        )

    return transition_block(block_id, RUNNING)


def complete_block(block_id: str) -> str:
    return transition_block(block_id, COMPLETED)


def begin_verification(block_id: str) -> str:
    return transition_block(block_id, VERIFYING)


def verify_block(block_id: str) -> str:
    return transition_block(block_id, VERIFIED)


def mark_backup_completed(block_id: str) -> str:
    return transition_block(block_id, BACKED_UP)


def approve_block(block_id: str) -> str:
    return transition_block(block_id, APPROVED)


def fail_block(block_id: str) -> str:
    return transition_block(block_id, FAILED)
