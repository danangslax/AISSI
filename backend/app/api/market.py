from pathlib import Path

import pandas as pd
from fastapi import APIRouter

router = APIRouter()

SNAPSHOT_DIR = Path("data/snapshots")


def get_latest_snapshot(category: str):

    category_dir = SNAPSHOT_DIR / category

    files = sorted(category_dir.glob("*.parquet"))

    if not files:
        return None

    latest_file = files[-1]

    df = pd.read_parquet(latest_file)

    return df.to_dict(orient="records")


# =========================================
# HEALTH CHECK
# =========================================


@router.get("/health")
async def health():

    return {"status": "ok"}


# =========================================
# MARKET REGIME
# =========================================


@router.get("/market-regime")
async def market_regime():

    data = get_latest_snapshot("market_regime")

    return data


# =========================================
# SCREENER
# =========================================


@router.get("/screener")
async def screener():

    data = get_latest_snapshot("screener")

    return data


# =========================================
# SECTOR ROTATION
# =========================================


@router.get("/sector-rotation")
async def sector_rotation():

    data = get_latest_snapshot("sector_rotation")

    return data


@router.get("/ai-signals")
async def ai_signals():

    data = get_latest_snapshot("ai_signal")

    return data
