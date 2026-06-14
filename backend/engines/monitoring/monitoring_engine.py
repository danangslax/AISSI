from pathlib import Path

import pandas as pd

from loguru import logger

from engines.telegram.telegram_engine import TelegramEngine
from app.utils.snapshot_manager import SnapshotManager

AI_SIGNAL_PATH = Path("data/snapshots/ai_signal/latest.parquet")

REGIME_PATH = Path("data/snapshots/market_regime/latest.parquet")


class MonitoringEngine:

    def __init__(self):

        self.telegram = TelegramEngine()

    # =========================================
    # BREAKOUT MONITOR
    # =========================================

    def monitor_breakout(self):

        try:

            if not AI_SIGNAL_PATH.exists():

                logger.warning("AI signal snapshot missing")

                return

            df = pd.read_parquet(AI_SIGNAL_PATH)

            breakout_df = df[df["confidence"] >= 80]

            if breakout_df.empty:

                logger.info("No breakout signals")

                return

            message = "AISSI BREAKOUT ALERT\n\n"

            for _, row in breakout_df.iterrows():

                message += f"{row['symbol']}\n"

                message += f"Signal : " f"{row['signal']}\n"

                message += f"Confidence : " f"{row['confidence']}%\n"

                message += f"Reasons : " f"{row['reasons']}\n\n"

            self.telegram.send(message)

            logger.success("Breakout alert sent")

        except Exception as e:

            logger.error(f"Breakout monitor failed: {e}")

    # =========================================
    # REGIME MONITOR
    # =========================================

    def monitor_regime(self):

        try:

            snapshot = SnapshotManager()

            data = snapshot.load_latest("market_regime")

            if not data:

                logger.warning("Regime snapshot missing")

                return

            latest = data[0]

            regime = latest["regime"]

            message = "AISSI MARKET REGIME\n\n"

            message += f"Current Regime : " f"{regime}\n"

            message += f"RSI : " f"{latest['rsi']}\n"

            message += f"Close : " f"{latest['close']}\n"

            self.telegram.send(message)

            logger.success("Regime alert sent")

        except Exception as e:

            logger.error(f"Regime monitor failed: {e}")

    # =========================================
    # RUN ALL MONITORS
    # =========================================

    def run(self):

        logger.info("RUNNING MARKET MONITOR")

        self.monitor_breakout()

        self.monitor_regime()

        logger.success("MARKET MONITOR COMPLETED")
