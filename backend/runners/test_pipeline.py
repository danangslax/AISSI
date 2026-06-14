import time

from loguru import logger

# =========================================
# IMPORT RUNNERS
# =========================================

from runners.run_downloader import main as run_downloader

from runners.run_indicators import main as run_indicators

from runners.run_market_regime import main as run_market_regime

from runners.run_screener import main as run_screener

from runners.run_sector_rotation import main as run_sector_rotation

from runners.run_ai_signal import main as run_ai_signal

from runners.run_commentary import main as run_commentary

from runners.run_telegram_alert import main as run_telegram_alert

# =========================================
# TEST RESULTS
# =========================================

TOTAL_TESTS = 0

PASSED_TESTS = 0

FAILED_TESTS = 0


# =========================================
# TEST HELPER
# =========================================


def run_test(test_name: str, function):

    global TOTAL_TESTS
    global PASSED_TESTS
    global FAILED_TESTS

    TOTAL_TESTS += 1

    logger.info(f"RUNNING: {test_name}")

    start = time.time()

    try:

        function()

        duration = round(time.time() - start, 2)

        PASSED_TESTS += 1

        logger.success(f"SUCCESS: {test_name} " f"({duration}s)")

    except Exception as e:

        FAILED_TESTS += 1

        logger.error(f"FAILED: {test_name}")

        logger.error(e)


# =========================================
# MAIN TEST PIPELINE
# =========================================


def main():

    logger.info("==================================")

    logger.info("AISSI PIPELINE TEST STARTED")

    logger.info("==================================")

    pipeline_start = time.time()

    # =====================================
    # DOWNLOADER
    # =====================================

    run_test("DOWNLOADER", run_downloader)

    # =====================================
    # INDICATORS
    # =====================================

    run_test("INDICATORS", run_indicators)

    # =====================================
    # MARKET REGIME
    # =====================================

    run_test("MARKET REGIME", run_market_regime)

    # =====================================
    # SCREENER
    # =====================================

    run_test("SCREENER", run_screener)

    # =====================================
    # SECTOR ROTATION
    # =====================================

    run_test("SECTOR ROTATION", run_sector_rotation)

    # =====================================
    # AI SIGNAL
    # =====================================

    run_test("AI SIGNAL", run_ai_signal)

    # =====================================
    # COMMENTARY
    # =====================================

    run_test("COMMENTARY", run_commentary)

    # =====================================
    # TELEGRAM ALERT
    # =====================================

    run_test("TELEGRAM ALERT", run_telegram_alert)

    # =====================================
    # SUMMARY
    # =====================================

    total_duration = round(time.time() - pipeline_start, 2)

    logger.info("==================================")

    logger.success("AISSI PIPELINE TEST COMPLETED")

    logger.info("==================================")

    logger.info(f"TOTAL TESTS : {TOTAL_TESTS}")

    logger.info(f"PASSED      : {PASSED_TESTS}")

    logger.info(f"FAILED      : {FAILED_TESTS}")

    logger.info(f"DURATION    : " f"{total_duration}s")

    logger.info("==================================")


if __name__ == "__main__":

    main()
