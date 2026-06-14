from pathlib import Path

import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange
from loguru import logger

PARQUET_DIR = Path("data/parquet")
FEATURE_DIR = Path("data/features")

FEATURE_DIR.mkdir(parents=True, exist_ok=True)


class IndicatorEngine:

    def process_symbol(self, symbol: str):

        try:

            file_path = PARQUET_DIR / f"{symbol}.parquet"

            if not file_path.exists():
                logger.warning(f"Missing parquet: {symbol}")
                return

            logger.info(f"Processing indicators: {symbol}")

            df = pd.read_parquet(file_path)

            # normalize columns jadi Series 1D
            for col in ["Open", "High", "Low", "Close", "Volume"]:
                df[col] = df[col].squeeze()

            # EMA
            df["ema20"] = EMAIndicator(close=df["Close"], window=20).ema_indicator()

            df["ema50"] = EMAIndicator(close=df["Close"], window=50).ema_indicator()

            # RSI
            df["rsi"] = RSIIndicator(close=df["Close"], window=14).rsi()

            # MACD
            macd = MACD(close=df["Close"])

            df["macd"] = macd.macd()
            df["macd_signal"] = macd.macd_signal()

            # ATR
            atr = AverageTrueRange(
                high=df["High"], low=df["Low"], close=df["Close"], window=14
            )

            df["atr"] = atr.average_true_range()

            # Relative Volume
            df["volume_ma20"] = df["Volume"].rolling(20).mean()

            df["relative_volume"] = df["Volume"] / df["volume_ma20"]

            output_path = FEATURE_DIR / f"{symbol}.parquet"

            df.to_parquet(output_path)

            logger.success(f"Features saved: {symbol}")

        except Exception as e:
            logger.error(f"Indicator failed {symbol}: {e}")

    def run(self, symbols: list[str]):

        for symbol in symbols:
            self.process_symbol(symbol)
