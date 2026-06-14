from loguru import logger

from engines.ai_signal.ai_signal_engine import AISignalEngine

from engines.downloader.symbols import IDX_STOCKS


def main():

    logger.info("RUNNING AI SIGNAL ENGINE")

    engine = AISignalEngine()

    results = engine.run(IDX_STOCKS)

    if not results:

        logger.warning("No AI signals generated")

        return

    logger.success("AI SIGNAL ENGINE COMPLETED")

    logger.info(f"Total Signals : " f"{len(results)}")

    logger.info("SAMPLE SIGNALS")

    for result in results[:5]:

        logger.info(result)


if __name__ == "__main__":

    main()
