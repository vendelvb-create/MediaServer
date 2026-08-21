from pathlib import Path
import json

from path_safety import safe_path


def get_state_file() -> Path:
    """Returnerer sikker fil for blokkstatus."""
    return safe_path("_Data/block_state.json")


def load_state() -> dict:
    """Laster blokkstatus. Returnerer tom status hvis filen ikke finnes."""
    state_file = get_state_file()

    if not state_file.exists():
        return {}

    with state_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(state: dict) -> None:
    """Lagrer blokkstatus."""
    state_file = get_state_file()
    state_file.parent.mkdir(parents=True, exist_ok=True)

    with state_file.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2, ensure_ascii=False)
