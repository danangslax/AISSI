from apscheduler.schedulers.blocking import BlockingScheduler

from loguru import logger

from jobs.nightly_job import run_nightly_pipeline

from runners.run_monitoring import main as run_monitoring

# =========================================
# SCHEDULER
# =========================================

scheduler = BlockingScheduler()


# =========================================
# JOB WRAPPERS
# =========================================


def monitoring_job():

    logger.info("RUNNING MONITORING JOB")

    try:

        run_monitoring()

        logger.success("MONITORING JOB COMPLETED")

    except Exception as e:

        logger.error(f"Monitoring job failed: {e}")


def nightly_job():

    logger.info("RUNNING NIGHTLY PIPELINE")

    try:

        run_nightly_pipeline()

        logger.success("NIGHTLY PIPELINE COMPLETED")

    except Exception as e:

        logger.error(f"Nightly pipeline failed: {e}")


# =========================================
# JOBS
# =========================================

# Nightly pipeline
scheduler.add_job(
    nightly_job,
    "cron",
    hour=19,
    minute=0,
)

# Monitoring engine
scheduler.add_job(
    monitoring_job,
    "interval",
    minutes=30,
)


# =========================================
# START SCHEDULER
# =========================================

logger.success("AISSI Scheduler Started")

logger.info("Nightly pipeline scheduled " "at 19:00")

logger.info("Monitoring scheduled " "every 30 minutes")


scheduler.start()
