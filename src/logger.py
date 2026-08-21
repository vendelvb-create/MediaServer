from pathlib import Path
import logging


def get_log_dir() -> Path:
    """Returnerer den godkjente testmappen for logger."""
    return (Path.home() / "Desktop" / "Medialibrary_test" / "_Logs").resolve()


def get_logger(name: str = "mediaserver") -> logging.Logger:
    """
    Oppretter en grunnleggende logger.

    Loggeren skriver til testmiljøets _Logs-mappe.
    Ingen andre deler av systemet kobles inn ennå.
    """
    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        log_file = log_dir / "mediaserver.log"

        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
