from sqlalchemy.exc import SQLAlchemyError

from config import Config
from clients import AlphavantageClient
from common.logging import Logger
from errors import ApiClientError
from models import FinancialDataDB

logger = Logger()


def main():
    logger.info(f'Starting Get RAW Data for {Config.service_name} ...')
    db = FinancialDataDB(Config.finance_database_url)
    symbols = ["IBM", "AAPL"]

    try:
        for symbol in symbols:
            finance_api_client = AlphavantageClient()
            raw_data = finance_api_client.get_raw_data(symbol)
            logger.info(f'Successfully Retrieved RAW Data for {symbol} ...')
            process_data = finance_api_client.process_raw_data(symbol, raw_data, Config.finance_api_client_data_duration)
            db.add_financial_data(process_data)
            logger.info(f'Successfully Stored Processed Finance Data for {symbol} ...')
        logger.info(f'Complete Migration of RAW Data From Finance API to Database...')
    except ApiClientError as e:
        logger.error(f'Failed to Get RAW Data From API... Error:{e}')
    except SQLAlchemyError as e:
        logger.error(f"Failed to insert data into database... Error:{e}")


if __name__ == '__main__':
    main()