from pathlib import Path
import logging

from path_safety import get_test_root, safe_path


def get_log_dir() -> Path:
    """Returnerer godkjent loggmappe innenfor testroten."""
    return safe_path("_Logs")


def get_logger(name: str = "mediaserver") -> logging.Logger:
    """
    Oppretter en grunnleggende logger.

    Loggeren skriver til testmiljøets _Logs-mappe.
    Alle filstier valideres gjennom safe_path().
    """
    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        log_file = safe_path("_Logs/mediaserver.log")

        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
