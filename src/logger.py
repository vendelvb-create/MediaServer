from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import logging
from typing import Any

from path_safety import safe_path


def get_log_dir() -> Path:
    """Returnerer godkjent loggmappe innenfor testroten."""
    return safe_path("_Logs")


def get_logger(name: str = "mediaserver") -> logging.Logger:
    """
    Returnerer prosjektets grunnleggende logger.

    Loggeren skriver til _Logs/mediaserver.log.
    Alle filstier valideres gjennom safe_path().
    """
    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        log_file = safe_path("_Logs/mediaserver.log")

        handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def _timestamp() -> str:
    """Returnerer nåværende UTC-tid i ISO 8601-format."""
    return datetime.now(timezone.utc).isoformat()


def _format_value(value: Any) -> str:
    """Gjør loggverdier menneskelesbare."""
    if value is None:
        return "N/A"

    if isinstance(value, (list, tuple, set)):
        if not value:
            return "None"
        return ", ".join(str(item) for item in value)

    if isinstance(value, dict):
        if not value:
            return "None"
        return ", ".join(
            f"{key}={value[key]}"
            for key in value
        )

    return str(value)


@dataclass
class BuildLog:
    """
    Strukturert logg for én build/block-operasjon.

    Dekker minimumskravene i prosjektspesifikasjonen:
    timestamp, block ID, start/end, operation, data sources,
    downloads, cache usage, API requests, retries, errors,
    warnings, processed/skipped, final result og verification result.
    """

    block_id: str
    operation: str
    data_sources: list[str] = field(default_factory=list)

    downloads: int = 0
    cache_usage: str = "NOT_USED"
    api_requests: int = 0
    retry_attempts: int = 0

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    items_processed: int = 0
    items_skipped: int = 0

    final_result: str = "NOT_FINISHED"
    verification_result: str = "NOT_VERIFIED"

    start_time: str = field(default_factory=_timestamp)
    end_time: str | None = None
    duration: str | None = None

    def _calculate_duration(self) -> None:
        """Beregner varighet fra start- og sluttid."""
        if self.end_time is None:
            return

        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)

        seconds = (end - start).total_seconds()

        self.duration = f"{seconds:.3f}s"

    def finish(
        self,
        final_result: str,
        verification_result: str = "NOT_VERIFIED",
    ) -> None:
        """
        Avslutter build-operasjonen normalt.

        EndTime og Duration blir alltid registrert.
        """
        self.end_time = _timestamp()
        self.final_result = final_result
        self.verification_result = verification_result
        self._calculate_duration()

    def fail(self, error: str) -> None:
        """
        Registrerer en kritisk feil.

        Feilen blir lagret umiddelbart, og siste kjente timestamp
        beholdes selv om operasjonen ikke avsluttes normalt.
        """
        self.errors.append(error)
        self.final_result = "FAILED"

        if self.end_time is None:
            self.end_time = _timestamp()

        self._calculate_duration()

    def add_error(self, error: str) -> None:
        """Registrerer en feil."""
        self.errors.append(str(error))

    def add_warning(self, warning: str) -> None:
        """Registrerer en advarsel."""
        self.warnings.append(str(warning))

    def set_verification_result(self, result: str) -> None:
        """Registrerer eksplisitt verifikasjonsresultat."""
        self.verification_result = str(result)

    def to_text(self) -> str:
        """
        Returnerer hele build-loggen i menneskelesbart format.
        """
        errors = (
            "\n".join(
                f"  - {error}"
                for error in self.errors
            )
            if self.errors
            else "  - None"
        )

        warnings = (
            "\n".join(
                f"  - {warning}"
                for warning in self.warnings
            )
            if self.warnings
            else "  - None"
        )

        return (
            "============================================================\n"
            "MediaServer Build Log\n"
            "============================================================\n"
            f"Timestamp: {self.start_time}\n"
            f"Build/Block ID: {self.block_id}\n"
            f"Operation: {self.operation}\n"
            f"StartTime: {self.start_time}\n"
            f"EndTime: {_format_value(self.end_time)}\n"
            f"Duration: {_format_value(self.duration)}\n"
            f"Data Sources: {_format_value(self.data_sources)}\n"
            f"Downloads: {self.downloads}\n"
            f"Cache Usage: {self.cache_usage}\n"
            f"API Requests: {self.api_requests}\n"
            f"Retry Attempts: {self.retry_attempts}\n"
            f"Items Processed: {self.items_processed}\n"
            f"Items Skipped: {self.items_skipped}\n"
            "\n"
            "Errors:\n"
            f"{errors}\n"
            "\n"
            "Warnings:\n"
            f"{warnings}\n"
            "\n"
            f"Final Result: {self.final_result}\n"
            f"Verification Result: {self.verification_result}\n"
            "============================================================\n"
        )

    def write(self) -> Path:
        """
        Skriver build-loggen til _Logs/.

        Returnerer den sikre loggfilens sti.
        """
        log_dir = get_log_dir()
        log_dir.mkdir(parents=True, exist_ok=True)

        safe_block_id = (
            self.block_id
            .replace("\\", "_")
            .replace("/", "_")
            .replace(":", "_")
        )

        timestamp = datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%SZ"
        )

        log_file = safe_path(
            f"_Logs/build_{safe_block_id}_{timestamp}.log"
        )

        log_file.write_text(
            self.to_text(),
            encoding="utf-8",
        )

        return log_file


def start_build_log(
    block_id: str,
    operation: str,
    data_sources: list[str] | None = None,
) -> BuildLog:
    """
    Oppretter en ny build-logg.

    StartTime registreres umiddelbart.
    """
    return BuildLog(
        block_id=block_id,
        operation=operation,
        data_sources=list(data_sources or []),
    )


def log_build_complete(
    build_log: BuildLog,
    final_result: str,
    verification_result: str,
) -> Path:
    """
    Avslutter og skriver en vellykket build-logg.
    """
    build_log.finish(
        final_result=final_result,
        verification_result=verification_result,
    )

    return build_log.write()


def log_build_failure(
    build_log: BuildLog,
    error: str,
) -> Path:
    """
    Registrerer kritisk feil og skriver failure-loggen.

    Dette sikrer at feil blir bevart selv når en build stopper
    før normal avslutning.
    """
    build_log.fail(error)

    return build_log.write()