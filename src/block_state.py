from pathlib import Path
import json

from path_safety import safe_path


# States defined by the project specification.
NOT_STARTED = "NOT_STARTED"
RUNNING = "RUNNING"
FAILED = "FAILED"
COMPLETED = "COMPLETED"
VERIFYING = "VERIFYING"
VERIFIED = "VERIFIED"
BACKED_UP = "BACKED_UP"
APPROVED = "APPROVED"


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


# Only these state transitions are allowed.
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
    """Returnerer sikker fil for blokkstatus."""
    return safe_path("_Data/block_state.json")


def load_state() -> dict:
    """Laster blokkstatus. Returnerer tom status hvis filen ikke finnes."""
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
    """Lagrer blokkstatus."""
    if not isinstance(state, dict):
        raise ValueError("Block state must be a dictionary.")

    state_file = get_state_file()
    state_file.parent.mkdir(parents=True, exist_ok=True)

    with state_file.open("w", encoding="utf-8") as file:
        json.dump(
            state,
            file,
            indent=2,
            ensure_ascii=False,
        )


def _get_blocks(state: dict) -> dict:
    """Returnerer blokkseksjonen fra state."""
    blocks = state.get("blocks", {})

    if not isinstance(blocks, dict):
        raise ValueError("Block state 'blocks' must be a dictionary.")

    return blocks


def _get_block_entry(state: dict, block_id: str) -> dict:
    """Returnerer state-entry for en blokk."""
    if not isinstance(block_id, str) or not block_id.strip():
        raise ValueError("block_id must be a non-empty string.")

    blocks = _get_blocks(state)
    entry = blocks.get(block_id)

    if entry is None:
        return {
            "state": NOT_STARTED,
        }

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
    """
    Returnerer nåværende state for en blokk.

    En blokk som ikke finnes i state-filen regnes som NOT_STARTED.
    """
    state = load_state()
    entry = _get_block_entry(state, block_id)
    return entry["state"]


def _save_block_state(
    state: dict,
    block_id: str,
    new_state: str,
) -> None:
    """Lagrer en validert state for en blokk."""
    if new_state not in BLOCK_STATES:
        raise ValueError(f"Invalid block state: {new_state}")

    blocks = _get_blocks(state)

    entry = blocks.get(block_id)

    if entry is None:
        entry = {}

    if not isinstance(entry, dict):
        raise ValueError(
            f"State for block {block_id} must be a dictionary."
        )

    entry["state"] = new_state
    blocks[block_id] = entry
    state["blocks"] = blocks

    save_state(state)


def transition_block(block_id: str, new_state: str) -> str:
    """
    Utfører en eksplisitt og validert state transition.

    Ugyldige transitions blir avvist.
    """
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

    allowed_states = STATE_TRANSITIONS[current_state]

    if new_state not in allowed_states:
        raise ValueError(
            f"Invalid state transition for block {block_id}: "
            f"{current_state} -> {new_state}"
        )

    _save_block_state(state, block_id, new_state)

    return new_state


def _previous_block_id(block_id: str) -> str | None:
    """
    Returnerer forrige blokk basert på 1000-posisjons intervaller.

    Eksempel:
    0001-1000 -> None
    1001-2000 -> 0001-1000
    2001-3000 -> 1001-2000
    """
    if not isinstance(block_id, str):
        raise ValueError("block_id must be a string.")

    parts = block_id.split("-")

    if len(parts) != 2:
        raise ValueError(
            f"Invalid block id format: {block_id}"
        )

    try:
        start = int(parts[0])
        end = int(parts[1])
    except ValueError as exc:
        raise ValueError(
            f"Invalid block id format: {block_id}"
        ) from exc

    if start < 1 or end < start:
        raise ValueError(
            f"Invalid block range: {block_id}"
        )

    if end - start != 999:
        raise ValueError(
            f"Block must contain exactly 1000 positions: {block_id}"
        )

    if start == 1:
        return None

    previous_start = start - 1000
    previous_end = start - 1

    return f"{previous_start:04d}-{previous_end:04d}"


def can_start_block(block_id: str, user_approved: bool = False) -> bool:
    """
    Kontrollerer om en blokk kan startes.

    Krav:
    - Blokken må være NOT_STARTED.
    - Brukeren må eksplisitt godkjenne starten.
    - For alle blokker etter første må forrige blokk være APPROVED.
    """
    if not user_approved:
        return False

    current_state = get_block_state(block_id)

    if current_state != NOT_STARTED:
        return False

    state = load_state()
    previous_block = _previous_block_id(block_id)

    if previous_block is None:
        return True

    previous_state = _get_block_entry(
        state,
        previous_block,
    )["state"]

    return previous_state == APPROVED


def start_block(block_id: str, user_approved: bool = False) -> str:
    """
    Starter en blokk etter at sikkerhetskravene er kontrollert.

    Neste blokk kan ikke starte før forrige blokk er APPROVED.
    Første blokk krever også eksplisitt user_approved=True.
    """
    if not can_start_block(
        block_id,
        user_approved=user_approved,
    ):
        raise ValueError(
            f"Block {block_id} cannot be started. "
            "The block must be NOT_STARTED, the user must explicitly "
            "approve the start, and the previous block must be APPROVED."
        )

    return transition_block(
        block_id,
        RUNNING,
    )


def complete_block(block_id: str) -> str:
    """Markerer en blokk som ferdig bygget."""
    return transition_block(
        block_id,
        COMPLETED,
    )


def begin_verification(block_id: str) -> str:
    """Starter eksplisitt verifisering av en ferdig blokk."""
    return transition_block(
        block_id,
        VERIFYING,
    )


def verify_block(block_id: str) -> str:
    """Markerer en blokk som VERIFIED etter eksplisitt verifisering."""
    return transition_block(
        block_id,
        VERIFIED,
    )


def mark_backup_completed(block_id: str) -> str:
    """Markerer at backup av en verifisert blokk er ferdig."""
    return transition_block(
        block_id,
        BACKED_UP,
    )


def approve_block(block_id: str) -> str:
    """
    Godkjenner en blokk etter at den er VERIFIED og BACKED_UP.

    APPROVED er den eneste tilstanden som tillater neste blokk.
    """
    return transition_block(
        block_id,
        APPROVED,
    )


def fail_block(block_id: str) -> str:
    """
    Marker en RUNNING eller VERIFYING blokk som FAILED.

    FAILED stopper videre progresjon for blokken.
    """
    return transition_block(
        block_id,
        FAILED,
    )