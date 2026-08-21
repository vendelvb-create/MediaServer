from pathlib import Path

import pytest

from path_safety import get_test_root, safe_path


def test_safe_path_accepts_path_inside_root():
    root = get_test_root()
    candidate = root / "Movies"

    assert safe_path(candidate) == candidate.resolve()


def test_safe_path_rejects_path_outside_root():
    outside = Path.home() / "Documents"

    with pytest.raises(ValueError):
        safe_path(outside)


def test_safe_path_rejects_parent_traversal():
    with pytest.raises(ValueError):
        safe_path("../outside")


def test_safe_path_rejects_windows_parent_traversal():
    with pytest.raises(ValueError):
        safe_path(r"..\..\Windows\System32")
