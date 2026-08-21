import json

import pytest

from block_state import get_state_file, load_state, save_state


def test_get_state_file_is_inside_test_root():
    state_file = get_state_file()

    assert state_file == state_file.resolve()
    assert "_Data" in state_file.parts
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
        state_file.parent.rmdir()

    save_state({"test": True})

    assert state_file.exists()
    assert json.loads(
        state_file.read_text(encoding="utf-8")
    ) == {"test": True}