from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from app.api.market import router as market_router

# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="AISSI Backend",
    description=("AI-Assisted Swing Trading " "Platform for IDX"),
    version="1.0.0",
)


# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# API ROUTERS
# =========================================

app.include_router(market_router)


# =========================================
# ROOT ENDPOINT
# =========================================


@app.get("/")
async def root():

    return {
        "message": ("AISSI backend running"),
        "status": "online",
        "version": "1.0.0",
    }


# =========================================
# STARTUP EVENT
# =========================================


@app.on_event("startup")
async def startup_event():

    logger.info("===================================")

    logger.success("AISSI BACKEND STARTED")

    logger.info("Docs : " "http://127.0.0.1:8000/docs")

    logger.info("===================================")


# =========================================
# SHUTDOWN EVENT
# =========================================


@app.on_event("shutdown")
async def shutdown_event():

    logger.warning("===================================")

    logger.warning("AISSI BACKEND STOPPED")

    logger.warning("===================================")
