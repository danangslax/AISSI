from engines.backtest.backtest_engine import BacktestEngine
from engines.downloader.symbols import IDX_STOCKS


def main():

    engine = BacktestEngine()

    engine.run(IDX_STOCKS)


if __name__ == "__main__":
    main()
