from pathlib import Path

import pandas as pd

from loguru import logger

from engines.market_regime.regime_engine import MarketRegimeEngine

from app.utils.snapshot_manager import SnapshotManager

FEATURE_DIR = Path("data/features")


class ScreenerEngine:

    # =====================================
    # GET MARKET REGIME
    # =====================================

    def get_market_regime(self):

        regime_engine = MarketRegimeEngine()

        result = regime_engine.detect_regime()

        if not result:

            logger.warning("Failed to detect regime")

            return "sideways"

        return result["regime"]

    # =====================================
    # CALCULATE SCORE
    # =====================================

    def calculate_score(self, latest, regime):

        score = 0

        close = latest["Close"]

        ema20 = latest["ema20"]

        ema50 = latest["ema50"]

        rsi = latest["rsi"]

        macd = latest["macd"]

        macd_signal = latest["macd_signal"]

        relative_volume = latest["relative_volume"]

        atr = latest["atr"]

        # =================================
        # BULLISH
        # =================================

        if regime == "bullish":

            if close > ema20:

                score += 20

            if ema20 > ema50:

                score += 20

            if rsi > 60:

                score += 20

            if macd > macd_signal:

                score += 20

            if relative_volume > 1.5:

                score += 20

        # =================================
        # CAUTIOUS BULLISH
        # =================================

        elif regime == "cautious_bullish":

            if close > ema50:

                score += 20

            if rsi > 50:

                score += 15

            if macd > macd_signal:

                score += 15

            if relative_volume > 1.2:

                score += 10

        # =================================
        # SIDEWAYS
        # =================================

        elif regime == "sideways":

            if 40 <= rsi <= 60:

                score += 20

            if close > ema50:

                score += 15

            if atr < close * 0.03:

                score += 20

        # =================================
        # BEARISH
        # =================================

        elif regime == "bearish":

            if close > ema50:

                score += 10

            if rsi > 50:

                score += 10

            if relative_volume > 1.5:

                score += 5

        # =================================
        # PANIC
        # =================================

        elif regime == "panic":

            score = 0

        return score

    # =====================================
    # PROCESS SYMBOL
    # =====================================

    def process_symbol(self, symbol: str):

        try:

            file_path = FEATURE_DIR / f"{symbol}.parquet"

            if not file_path.exists():

                logger.warning(f"Missing feature file: " f"{symbol}")

                return None

            df = pd.read_parquet(file_path)

            latest = df.iloc[-1]

            score = self.calculate_score(latest, self.market_regime)

            result = {
                "symbol": symbol,
                "close": round(float(latest["Close"]), 2),
                "rsi": round(float(latest["rsi"]), 2),
                "score": score,
                "regime": (self.market_regime),
            }

            return result

        except Exception as e:

            logger.error(f"Screener failed " f"{symbol}: {e}")

            return None

    # =====================================
    # RUN SCREENER
    # =====================================

    def run(self, symbols: list[str]):

        self.market_regime = self.get_market_regime()

        logger.info(f"Current regime: " f"{self.market_regime}")

        results = []

        for symbol in symbols:

            result = self.process_symbol(symbol)

            if result:

                results.append(result)

        if not results:

            logger.warning("No screener results")

            return None

        screener_df = pd.DataFrame(results)

        screener_df = screener_df.sort_values(by="score", ascending=False)

        logger.success("SCREENER COMPLETED")

        logger.info("TOP PICKS")

        logger.info(f"\n{screener_df.head()}")

        # =================================
        # SAVE SNAPSHOT
        # =================================

        snapshot = SnapshotManager()

        snapshot.save_dataframe(screener_df, "screener")

        logger.success("Screener snapshot saved")

        return screener_df
