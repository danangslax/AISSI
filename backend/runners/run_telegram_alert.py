from loguru import logger

from engines.telegram.telegram_engine import TelegramEngine

from app.utils.snapshot_manager import SnapshotManager


def main():

    logger.info("RUNNING TELEGRAM ALERT")

    # =====================================
    # LOAD LATEST AI SIGNAL SNAPSHOT
    # =====================================

    snapshot = SnapshotManager()

    data = snapshot.load_latest("ai_signal")

    if not data:

        logger.warning("AI signal snapshot missing")

        return

    # =====================================
    # CONVERT TO DATAFRAME
    # =====================================

    import pandas as pd

    df = pd.DataFrame(data)

    if df.empty:

        logger.warning("AI signal dataframe empty")

        return

    # =====================================
    # TELEGRAM ENGINE
    # =====================================

    telegram = TelegramEngine()

    top_signals = df.sort_values(by="confidence", ascending=False).head(3)

    # =====================================
    # BUILD MESSAGE
    # =====================================

    message = "AISSI AI ALERT\n\n"

    for _, row in top_signals.iterrows():

        message += f"{row['symbol']} → " f"{row['signal']}\n"

        message += f"Confidence : " f"{row['confidence']}%\n"

        message += f"Reasons : " f"{row['reasons']}\n\n"

    # =====================================
    # SEND TELEGRAM ALERT
    # =====================================

    telegram.send(message)

    logger.success("TELEGRAM ALERT SENT")


if __name__ == "__main__":

    main()
