from pathlib import Path

import pandas as pd

from loguru import logger

from app.utils.snapshot_manager import SnapshotManager

FEATURE_DIR = Path("data/features")


class MarketRegimeEngine:

    # =====================================
    # DETECT MARKET REGIME
    # =====================================

    def detect_regime(self):

        try:

            # =================================
            # LOAD IHSG FEATURE DATA
            # =================================

            file_path = FEATURE_DIR / "^JKSE.parquet"

            if not file_path.exists():

                logger.error("IHSG feature data missing")

                return None

            df = pd.read_parquet(file_path)

            latest = df.iloc[-1]

            # =================================
            # EXTRACT INDICATORS
            # =================================

            close = latest["Close"]

            ema20 = latest["ema20"]

            ema50 = latest["ema50"]

            rsi = latest["rsi"]

            # =================================
            # REGIME DETECTION
            # =================================

            regime = "sideways"

            if close > ema20 > ema50 and rsi >= 60:

                regime = "bullish"

            elif close > ema50 and rsi >= 50:

                regime = "cautious_bullish"

            elif close < ema20 < ema50 and rsi <= 40:

                regime = "bearish"

            elif rsi <= 30:

                regime = "panic"

            # =================================
            # RESULT
            # =================================

            result = {
                "regime": regime,
                "close": round(float(close), 2),
                "ema20": round(float(ema20), 2),
                "ema50": round(float(ema50), 2),
                "rsi": round(float(rsi), 2),
            }

            # =================================
            # LOGGING
            # =================================

            logger.success(f"Market Regime: " f"{regime}")

            logger.info(f"Regime Data: " f"{result}")

            # =================================
            # SAVE SNAPSHOT
            # =================================

            snapshot = SnapshotManager()

            snapshot.save_dict(result, "market_regime")

            logger.success("Market regime snapshot saved")

            return result

        except Exception as e:

            logger.error(f"Regime detection failed: " f"{e}")

            return None
