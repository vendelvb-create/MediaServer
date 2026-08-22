from pathlib import Path

from logger import (
    BuildLog,
    get_log_dir,
    get_logger,
    log_build_complete,
    log_build_failure,
    start_build_log,
)
from path_safety import get_test_root


def _cleanup_log_file(path: Path) -> None:
    """Fjerner en testgenerert loggfil hvis den finnes."""
    if path.exists():
        path.unlink()


def _close_logger_handlers(logger) -> None:
    """Lukker og fjerner loggerens handlers for Windows-kompatibel cleanup."""
    for handler in logger.handlers[:]:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)


def test_get_log_dir_is_inside_test_root():
    log_dir = get_log_dir()

    assert log_dir.resolve().is_relative_to(
        get_test_root().resolve()
    )
    assert log_dir.name == "_Logs"


def test_get_logger_creates_logger_and_log_file():
    logger = get_logger("test_logger")
    log_file = get_log_dir() / "mediaserver.log"

    try:
        logger.info("logger test message")

        for handler in logger.handlers:
            handler.flush()

        assert log_file.exists()

        content = log_file.read_text(
            encoding="utf-8"
        )

        assert "logger test message" in content
    finally:
        _close_logger_handlers(logger)
        _cleanup_log_file(log_file)


def test_start_build_log_records_required_initial_fields():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
        data_sources=["source_a", "source_b"],
    )

    assert build_log.block_id == "0001-1000"
    assert build_log.operation == "catalog build"
    assert build_log.data_sources == [
        "source_a",
        "source_b",
    ]

    assert build_log.start_time
    assert build_log.end_time is None
    assert build_log.duration is None

    assert build_log.downloads == 0
    assert build_log.cache_usage == "NOT_USED"
    assert build_log.api_requests == 0
    assert build_log.retry_attempts == 0

    assert build_log.errors == []
    assert build_log.warnings == []

    assert build_log.items_processed == 0
    assert build_log.items_skipped == 0

    assert build_log.final_result == "NOT_FINISHED"
    assert build_log.verification_result == "NOT_VERIFIED"


def test_build_log_records_operation_details():
    build_log = BuildLog(
        block_id="0001-1000",
        operation="catalog build",
        data_sources=["API", "local cache"],
        downloads=12,
        cache_usage="USED",
        api_requests=8,
        retry_attempts=2,
        items_processed=950,
        items_skipped=50,
    )

    build_log.add_warning("One item requires review.")
    build_log.add_error("One API request failed.")

    text = build_log.to_text()

    assert "Build/Block ID: 0001-1000" in text
    assert "Operation: catalog build" in text
    assert "Data Sources: API, local cache" in text
    assert "Downloads: 12" in text
    assert "Cache Usage: USED" in text
    assert "API Requests: 8" in text
    assert "Retry Attempts: 2" in text
    assert "Items Processed: 950" in text
    assert "Items Skipped: 50" in text
    assert "One item requires review." in text
    assert "One API request failed." in text


def test_build_log_finish_records_end_time_duration_and_results():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
    )

    build_log.finish(
        final_result="SUCCESS",
        verification_result="VERIFIED",
    )

    assert build_log.end_time is not None
    assert build_log.duration is not None
    assert build_log.final_result == "SUCCESS"
    assert build_log.verification_result == "VERIFIED"


def test_build_log_failure_records_error_and_timestamp():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
    )

    build_log.fail("Critical build failure.")

    assert build_log.end_time is not None
    assert build_log.duration is not None
    assert build_log.final_result == "FAILED"
    assert "Critical build failure." in build_log.errors


def test_build_log_add_error_and_warning():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="test operation",
    )

    build_log.add_error("Example error")
    build_log.add_warning("Example warning")

    assert build_log.errors == ["Example error"]
    assert build_log.warnings == ["Example warning"]


def test_build_log_verification_result_is_explicit():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="verification",
    )

    build_log.set_verification_result("FAILED")

    assert build_log.verification_result == "FAILED"


def test_log_build_complete_writes_human_readable_log():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
        data_sources=["test source"],
    )

    build_log.items_processed = 1000
    build_log.items_skipped = 0

    log_file = log_build_complete(
        build_log,
        final_result="SUCCESS",
        verification_result="VERIFIED",
    )

    try:
        assert log_file.exists()
        assert log_file.resolve().is_relative_to(
            get_test_root().resolve()
        )
        assert log_file.parent.name == "_Logs"

        content = log_file.read_text(
            encoding="utf-8"
        )

        assert "MediaServer Build Log" in content
        assert "Build/Block ID: 0001-1000" in content
        assert "Operation: catalog build" in content
        assert "StartTime:" in content
        assert "EndTime:" in content
        assert "Duration:" in content
        assert "Items Processed: 1000" in content
        assert "Items Skipped: 0" in content
        assert "Final Result: SUCCESS" in content
        assert "Verification Result: VERIFIED" in content
    finally:
        _cleanup_log_file(log_file)


def test_log_build_failure_writes_failure_log():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
    )

    log_file = log_build_failure(
        build_log,
        "CRITICAL: source unavailable.",
    )

    try:
        assert log_file.exists()

        content = log_file.read_text(
            encoding="utf-8"
        )

        assert "Build/Block ID: 0001-1000" in content
        assert "Final Result: FAILED" in content
        assert "CRITICAL: source unavailable." in content
        assert "EndTime:" in content
        assert "Duration:" in content
    finally:
        _cleanup_log_file(log_file)


def test_failure_log_contains_last_known_timestamp():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
    )

    original_start_time = build_log.start_time

    build_log.fail("Critical failure before normal completion.")

    assert build_log.start_time == original_start_time
    assert build_log.end_time is not None

    text = build_log.to_text()

    assert "StartTime:" in text
    assert "EndTime:" in text
    assert "Critical failure before normal completion." in text


def test_log_filename_is_safe_for_block_identifier():
    build_log = start_build_log(
        block_id="0001-1000/test",
        operation="catalog build",
    )

    log_file = log_build_complete(
        build_log,
        final_result="SUCCESS",
        verification_result="VERIFIED",
    )

    try:
        assert log_file.exists()
        assert log_file.resolve().is_relative_to(
            get_test_root().resolve()
        )
        assert "/" not in log_file.name
        assert "\\" not in log_file.name
    finally:
        _cleanup_log_file(log_file)


def test_log_build_complete_requires_explicit_verification_result():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
    )

    log_file = log_build_complete(
        build_log,
        final_result="SUCCESS",
        verification_result="NOT_VERIFIED",
    )

    try:
        content = log_file.read_text(
            encoding="utf-8"
        )

        assert "Final Result: SUCCESS" in content
        assert "Verification Result: NOT_VERIFIED" in content
    finally:
        _cleanup_log_file(log_file)


def test_empty_collections_are_human_readable():
    build_log = start_build_log(
        block_id="0001-1000",
        operation="catalog build",
        data_sources=[],
    )

    text = build_log.to_text()

    assert "Data Sources: None" in text
    assert "Errors:" in text
    assert "Warnings:" in text
    assert "  - None" in text