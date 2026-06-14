from engines.screener.screener_engine import ScreenerEngine
from engines.downloader.symbols import IDX_STOCKS


def main():

    engine = ScreenerEngine()

    engine.run(IDX_STOCKS)


if __name__ == "__main__":
    main()
