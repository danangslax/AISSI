from loguru import logger

from engines.risk_management.risk_engine import PortfolioRiskEngine


def main():

    logger.info("RUNNING RISK MANAGEMENT ENGINE")

    engine = PortfolioRiskEngine()

    # =====================================
    # POSITION SIZE
    # =====================================

    position_result = engine.calculate_position_size(
        capital=100_000_000,
        risk_per_trade_pct=1,
        entry_price=5000,
        stop_loss_price=4700,
    )

    # =====================================
    # RISK REWARD
    # =====================================

    risk_reward_result = engine.calculate_risk_reward(
        entry_price=5000,
        stop_loss_price=4700,
        take_profit_price=5900,
    )

    # =====================================
    # LOGGING
    # =====================================

    logger.success("RISK MANAGEMENT COMPLETED")

    logger.info("POSITION SIZE RESULT")

    logger.info(position_result)

    logger.info("RISK REWARD RESULT")

    logger.info(risk_reward_result)


if __name__ == "__main__":

    main()
