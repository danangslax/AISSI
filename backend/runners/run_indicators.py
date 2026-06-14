from engines.indicators.indicator_engine import IndicatorEngine
from engines.downloader.symbols import IDX_STOCKS, IDX_INDEX


def main():

    engine = IndicatorEngine()

    symbols = IDX_STOCKS + [IDX_INDEX]

    engine.run(symbols)


if __name__ == "__main__":
    main()
