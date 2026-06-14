from pathlib import Path

import pandas as pd

from loguru import logger

FEATURE_DIR = Path("data/features")


class BacktestEngine:

    # =====================================
    # GENERATE SIGNAL
    # =====================================

    def generate_signal(self, row):

        score = 0

        # =================================
        # TREND
        # =================================

        if row["Close"] > row["ema20"]:

            score += 20

        if row["ema20"] > row["ema50"]:

            score += 20

        # =================================
        # MOMENTUM
        # =================================

        if row["rsi"] > 60:

            score += 20

        # =================================
        # MACD
        # =================================

        if row["macd"] > row["macd_signal"]:

            score += 20

        # =================================
        # VOLUME
        # =================================

        if row["relative_volume"] > 1.5:

            score += 20

        return score >= 60

    # =====================================
    # BACKTEST SINGLE SYMBOL
    # =====================================

    def backtest_symbol(self, symbol: str):

        try:

            file_path = FEATURE_DIR / f"{symbol}.parquet"

            if not file_path.exists():

                logger.warning(f"Missing feature file: " f"{symbol}")

                return []

            df = pd.read_parquet(file_path)

            trades = []

            for i in range(50, len(df) - 5):

                row = df.iloc[i]

                signal = self.generate_signal(row)

                if not signal:

                    continue

                entry_price = float(row["Close"])

                future_price = float(df.iloc[i + 5]["Close"])

                return_pct = ((future_price - entry_price) / entry_price) * 100

                # =========================
                # ENTRY DATE
                # =========================

                if "Date" in row:

                    entry_date = str(row["Date"])

                else:

                    entry_date = str(df.index[i])

                trade = {
                    "symbol": symbol,
                    "entry_date": entry_date,
                    "entry_price": round(entry_price, 2),
                    "exit_price": round(future_price, 2),
                    "return_pct": round(float(return_pct), 2),
                    "win": return_pct > 0,
                }

                trades.append(trade)

            return trades

        except Exception as e:

            logger.error(f"Backtest failed " f"{symbol}: {e}")

            return []

    # =====================================
    # RUN BACKTEST
    # =====================================

    def run(self, symbols: list[str]):

        all_trades = []

        logger.info("RUNNING BACKTEST ENGINE")

        for symbol in symbols:

            trades = self.backtest_symbol(symbol)

            all_trades.extend(trades)

        if not all_trades:

            logger.warning("No backtest trades found")

            return None

        trades_df = pd.DataFrame(all_trades)

        winrate = (trades_df["win"].mean()) * 100

        avg_return = trades_df["return_pct"].mean()

        total_trades = len(trades_df)

        # =============================
        # SUMMARY
        # =============================

        logger.success("BACKTEST COMPLETED")

        logger.info(f"Total Trades : " f"{total_trades}")

        logger.info(f"Winrate      : " f"{winrate:.2f}%")

        logger.info(f"Avg Return   : " f"{avg_return:.2f}%")

        logger.info("SAMPLE TRADES")

        logger.info(f"\n{trades_df.head()}")

        return trades_df
