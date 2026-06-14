from pathlib import Path

import pandas as pd

from loguru import logger

FEATURE_DIR = Path("data/features")

SNAPSHOT_DIR = Path("data/snapshots/ai_signal")

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


class AISignalEngine:

    # =========================================
    # ANALYZE SINGLE SYMBOL
    # =========================================

    def analyze_symbol(self, symbol: str):

        try:

            file_path = FEATURE_DIR / f"{symbol}.parquet"

            if not file_path.exists():

                return None

            df = pd.read_parquet(file_path)

            latest = df.iloc[-1]

            confidence = 0

            reasons = []

            signal = "NEUTRAL"

            # =====================================
            # TREND
            # =====================================

            if latest["Close"] > latest["ema20"]:

                confidence += 20

                reasons.append("Price above EMA20")

            if latest["ema20"] > latest["ema50"]:

                confidence += 20

                reasons.append("EMA20 above EMA50")

            # =====================================
            # MOMENTUM
            # =====================================

            if latest["rsi"] > 60:

                confidence += 20

                reasons.append("Strong RSI momentum")

            elif latest["rsi"] < 40:

                confidence -= 10

                reasons.append("Weak RSI momentum")

            # =====================================
            # MACD
            # =====================================

            if latest["macd"] > latest["macd_signal"]:

                confidence += 20

                reasons.append("MACD bullish crossover")

            # =====================================
            # VOLUME
            # =====================================

            if latest["relative_volume"] > 1.5:

                confidence += 20

                reasons.append("High relative volume")

            # =====================================
            # SIGNAL CLASSIFICATION
            # =====================================

            if confidence >= 80:

                signal = "STRONG BUY"

            elif confidence >= 60:

                signal = "BUY"

            elif confidence >= 40:

                signal = "WATCHLIST"

            elif confidence < 20:

                signal = "AVOID"

            result = {
                "symbol": symbol,
                "signal": signal,
                "confidence": confidence,
                # IMPORTANT:
                # SAVE AS STRING
                "reasons": " | ".join(reasons),
            }

            return result

        except Exception as e:

            logger.error(f"AI signal failed {symbol}: {e}")

            return None

    # =========================================
    # RUN ALL SYMBOLS
    # =========================================

    def run(self, symbols: list[str]):

        results = []

        for symbol in symbols:

            result = self.analyze_symbol(symbol)

            if result:

                results.append(result)

        # =====================================
        # SAVE SNAPSHOT
        # =====================================

        if results:

            df = pd.DataFrame(results)

            output_path = SNAPSHOT_DIR / "latest.parquet"

            df.to_parquet(output_path)

            logger.success("AI signal snapshot saved")

        return results
