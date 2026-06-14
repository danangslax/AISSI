from engines.forward_testing.forward_tester import ForwardTester

from engines.downloader.symbols import IDX_STOCKS


def main():

    tester = ForwardTester()

    tester.run(IDX_STOCKS)


if __name__ == "__main__":
    main()
