from pathlib import Path

from path_safety import get_test_root, safe_path


def test_safe_path_accepts_path_inside_root():
    root = get_test_root()
    candidate = root / "Movies"
    assert safe_path(candidate) == candidate.resolve()


def test_safe_path_rejects_path_outside_root():
    outside = Path.home() / "Documents"
    
    try:
        safe_path(outside)
    except ValueError:
        pass
    else:
        raise AssertionError("Path outside test root was accepted")
