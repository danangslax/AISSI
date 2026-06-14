from loguru import logger

from engines.downloader.downloader import MarketDownloader

from engines.downloader.symbols import IDX_STOCKS, IDX_INDEX

from engines.indicators.indicator_engine import IndicatorEngine

from engines.market_regime.regime_engine import MarketRegimeEngine

from engines.screener.screener_engine import ScreenerEngine

from engines.sector_rotation.sector_rotation_engine import SectorRotationEngine


def run_nightly_pipeline():

    logger.info("STARTING NIGHTLY PIPELINE")

    symbols = IDX_STOCKS + [IDX_INDEX]

    # ====================================
    # DOWNLOAD MARKET DATA
    # ====================================

    downloader = MarketDownloader()

    downloader.run(symbols)

    # ====================================
    # CALCULATE INDICATORS
    # ====================================

    indicator_engine = IndicatorEngine()

    indicator_engine.run(symbols)

    # ====================================
    # MARKET REGIME
    # ====================================

    regime_engine = MarketRegimeEngine()

    regime_engine.detect_regime()

    # ====================================
    # SCREENER
    # ====================================

    screener = ScreenerEngine()

    screener.run(IDX_STOCKS)

    # ====================================
    # SECTOR ROTATION
    # ====================================

    sector_engine = SectorRotationEngine()

    sector_engine.process_sector()

    logger.success("NIGHTLY PIPELINE COMPLETED")


if __name__ == "__main__":

    run_nightly_pipeline()
