from engines.market_regime.regime_engine import MarketRegimeEngine


def main():

    engine = MarketRegimeEngine()

    engine.detect_regime()


if __name__ == "__main__":
    main()
