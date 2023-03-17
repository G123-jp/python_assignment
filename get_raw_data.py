from config import Config
from clients import AlphavantageClient
from common.logging import Logger

logger = Logger()


def main():
    logger.info(f'Starting Get RAW Data for {Config.service_name} ...')
    symbols = ["IBM", "AAPL"]
    for symbol in symbols:
        finance_api_client = AlphavantageClient()
        raw_data = finance_api_client.get_raw_data(symbol)
        process_data = finance_api_client.process_raw_data(symbol, raw_data, Config.finance_api_client_data_duration)

        print(raw_data)
        print(process_data)


if __name__ == '__main__':
    main()