from engines.downloader.downloader import MarketDownloader
from engines.downloader.symbols import IDX_STOCKS, IDX_INDEX


def main():

    downloader = MarketDownloader()

    symbols = IDX_STOCKS + [IDX_INDEX]

    downloader.run(symbols)


if __name__ == "__main__":
    main()
