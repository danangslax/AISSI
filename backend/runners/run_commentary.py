from loguru import logger

from engines.commentary.commentary_engine import CommentaryEngine

from engines.market_regime.regime_engine import MarketRegimeEngine

from engines.sector_rotation.sector_rotation_engine import SectorRotationEngine


def main():

    logger.info("RUNNING COMMENTARY ENGINE")

    # =====================================
    # MARKET REGIME
    # =====================================

    regime_engine = MarketRegimeEngine()

    regime_data = regime_engine.detect_regime()

    if not regime_data:

        logger.warning("Failed to detect regime")

        return

    # =====================================
    # SECTOR ROTATION
    # =====================================

    sector_engine = SectorRotationEngine()

    sector_df = sector_engine.process_sector()

    if sector_df is None:

        logger.warning("No sector rotation data")

        return

    top_sector = sector_df.iloc[0]["sector"]

    # =====================================
    # GENERATE COMMENTARY
    # =====================================

    commentary_engine = CommentaryEngine()

    commentary = commentary_engine.generate_market_commentary(regime_data, top_sector)

    if not commentary:

        logger.warning("No commentary generated")

        return

    # =====================================
    # LOGGING
    # =====================================

    logger.success("COMMENTARY GENERATED")

    logger.info("AI MARKET COMMENTARY")

    for line in commentary:

        logger.info(f"- {line}")


if __name__ == "__main__":

    main()
