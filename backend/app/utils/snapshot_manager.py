from pathlib import Path
from datetime import datetime

import pandas as pd
from loguru import logger

SNAPSHOT_DIR = Path("data/snapshots")

SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


class SnapshotManager:

    def save_dataframe(self, df: pd.DataFrame, category: str):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        category_dir = SNAPSHOT_DIR / category

        category_dir.mkdir(parents=True, exist_ok=True)

        output_path = category_dir / f"{timestamp}.parquet"

        df.to_parquet(output_path)

        logger.success(f"Snapshot saved: {output_path}")

        return output_path

    def save_dict(self, data: dict, category: str):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        category_dir = SNAPSHOT_DIR / category

        category_dir.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame([data])

        output_path = category_dir / f"{timestamp}.parquet"

        df.to_parquet(output_path)

        logger.success(f"Snapshot saved: {output_path}")

        return output_path

    def load_latest(self, category: str):

        try:

            category_dir = SNAPSHOT_DIR / category

            if not category_dir.exists():

                logger.warning(f"Snapshot folder missing: " f"{category}")

                return None

            files = sorted(category_dir.glob("*.parquet"), reverse=True)

            if not files:

                logger.warning(f"No snapshots found: " f"{category}")

                return None

            latest_file = files[0]

            df = pd.read_parquet(latest_file)

            logger.success(f"Loaded snapshot: " f"{latest_file}")

            return df.to_dict(orient="records")

        except Exception as e:

            logger.error(f"Load latest snapshot failed: {e}")

            return None
