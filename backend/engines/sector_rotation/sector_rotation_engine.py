from pathlib import Path

import pandas as pd

from loguru import logger

from engines.screener.sector_map import SECTOR_MAP

from app.utils.snapshot_manager import SnapshotManager

FEATURE_DIR = Path("data/features")


class SectorRotationEngine:

    # =====================================
    # PROCESS SECTOR ROTATION
    # =====================================

    def process_sector(self):

        sector_data = {}

        for symbol, sector in SECTOR_MAP.items():

            try:

                file_path = FEATURE_DIR / f"{symbol}.parquet"

                if not file_path.exists():

                    logger.warning(f"Missing feature file: " f"{symbol}")

                    continue

                df = pd.read_parquet(file_path)

                latest = df.iloc[-1]

                close = latest["Close"]

                ema20 = latest["ema20"]

                rsi = latest["rsi"]

                relative_volume = latest["relative_volume"]

                score = 0

                # =========================
                # TREND
                # =========================

                if close > ema20:

                    score += 30

                # =========================
                # MOMENTUM
                # =========================

                if rsi > 60:

                    score += 30

                elif rsi > 50:

                    score += 20

                # =========================
                # VOLUME
                # =========================

                if relative_volume > 1.2:

                    score += 40

                # =========================
                # SECTOR GROUPING
                # =========================

                if sector not in sector_data:

                    sector_data[sector] = {"scores": []}

                sector_data[sector]["scores"].append(score)

            except Exception as e:

                logger.error(f"Sector processing " f"failed {symbol}: {e}")

        # =================================
        # CALCULATE AVERAGE SCORE
        # =================================

        results = []

        for sector, data in sector_data.items():

            avg_score = sum(data["scores"]) / len(data["scores"])

            results.append(
                {
                    "sector": sector,
                    "score": round(float(avg_score), 2),
                }
            )

        if not results:

            logger.warning("No sector rotation results")

            return None

        sector_df = pd.DataFrame(results)

        sector_df = sector_df.sort_values(by="score", ascending=False)

        # =================================
        # LOGGING
        # =================================

        logger.success("SECTOR ROTATION COMPLETED")

        logger.info("TOP SECTORS")

        logger.info(f"\n{sector_df.head()}")

        # =================================
        # SAVE SNAPSHOT
        # =================================

        snapshot = SnapshotManager()

        snapshot.save_dataframe(sector_df, "sector_rotation")

        logger.success("Sector rotation snapshot saved")

        return sector_df
