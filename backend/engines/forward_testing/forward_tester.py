from pathlib import Path

import pandas as pd

from loguru import logger

FEATURE_DIR = Path("data/features")


class ForwardTester:

    # =====================================
    # EVALUATE SINGLE SYMBOL
    # =====================================

    def evaluate_symbol(self, symbol: str):

        try:

            file_path = FEATURE_DIR / f"{symbol}.parquet"

            if not file_path.exists():

                logger.warning(f"Missing feature file: " f"{symbol}")

                return []

            df = pd.read_parquet(file_path)

            evaluations = []

            for i in range(50, len(df) - 10):

                row = df.iloc[i]

                # =========================
                # SIGNAL LOGIC
                # =========================

                signal = (
                    row["Close"] > row["ema20"]
                    and row["ema20"] > row["ema50"]
                    and row["rsi"] > 60
                )

                if not signal:

                    continue

                entry_price = float(row["Close"])

                plus_3d = float(df.iloc[i + 3]["Close"])

                plus_5d = float(df.iloc[i + 5]["Close"])

                plus_10d = float(df.iloc[i + 10]["Close"])

                # =========================
                # RETURNS
                # =========================

                return_3d = ((plus_3d - entry_price) / entry_price) * 100

                return_5d = ((plus_5d - entry_price) / entry_price) * 100

                return_10d = ((plus_10d - entry_price) / entry_price) * 100

                # =========================
                # DATE SAFETY
                # =========================

                if "Date" in row:

                    entry_date = str(row["Date"])

                else:

                    entry_date = str(df.index[i])

                result = {
                    "symbol": symbol,
                    "date": entry_date,
                    "entry": round(entry_price, 2),
                    "return_3d": round(float(return_3d), 2),
                    "return_5d": round(float(return_5d), 2),
                    "return_10d": round(float(return_10d), 2),
                }

                evaluations.append(result)

            return evaluations

        except Exception as e:

            logger.error(f"Forward test failed " f"{symbol}: {e}")

            return []

    # =====================================
    # RUN FORWARD TEST
    # =====================================

    def run(self, symbols: list[str]):

        all_results = []

        logger.info("RUNNING FORWARD TESTER")

        for symbol in symbols:

            results = self.evaluate_symbol(symbol)

            all_results.extend(results)

        if not all_results:

            logger.warning("No forward test results")

            return None

        df = pd.DataFrame(all_results)

        # =============================
        # STATISTICS
        # =============================

        avg_3d = df["return_3d"].mean()

        avg_5d = df["return_5d"].mean()

        avg_10d = df["return_10d"].mean()

        # =============================
        # LOGGING
        # =============================

        logger.success("FORWARD TEST COMPLETED")

        logger.info(f"Avg +3D Return  : " f"{avg_3d:.2f}%")

        logger.info(f"Avg +5D Return  : " f"{avg_5d:.2f}%")

        logger.info(f"Avg +10D Return : " f"{avg_10d:.2f}%")

        logger.info("SAMPLE RESULTS")

        logger.info(f"\n{df.head()}")

        return df
