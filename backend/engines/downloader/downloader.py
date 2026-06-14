from pathlib import Path
import pandas as pd
import yfinance as yf
from loguru import logger

DATA_DIR = Path("data/parquet")
DATA_DIR.mkdir(parents=True, exist_ok=True)


class MarketDownloader:

    def download_stock(self, symbol: str, period="2y"):

        logger.info(f"Downloading {symbol}")

        try:

            df = yf.download(
                symbol,
                period=period,
                auto_adjust=True,
                progress=False,
            )

            # normalize multi-index columns
            df.columns = [
                col[0] if isinstance(col, tuple) else col for col in df.columns
            ]

            if df.empty:
                logger.warning(f"No data for {symbol}")
                return

            df = df.reset_index()

            output_path = DATA_DIR / f"{symbol}.parquet"

            df.to_parquet(output_path)

            logger.success(f"Saved {symbol}")

        except Exception as e:
            logger.error(f"Failed {symbol}: {e}")

    def run(self, symbols: list[str]):

        for symbol in symbols:
            self.download_stock(symbol)
