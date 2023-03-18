import os

from sqlalchemy.exc import SQLAlchemyError

from config import Config
from clients import AlphavantageClient
from common.logging import Logger
from errors import ApiClientError
from repository import FinancialRepository
from dotenv import load_dotenv

logger = Logger()
load_dotenv('.env')

finance_api_client_api_key = os.getenv('FINANCE_API_CLIENT_API_KEY')
finance_api_client_api_url = os.getenv('FINANCE_API_CLIENT_API_URL')
finance_api_client_data_duration = int(os.getenv('FINANCE_API_CLIENT_DATA_DURATION'))
finance_database_url = os.getenv('FINANCE_DATABASE_URL')
# create db file inside the project directory.
finance_database_url = finance_database_url[:len('sqlite:///')]+'financial/'+finance_database_url[len('sqlite:///'):]


def main():
    logger.info(f'Starting Get RAW Data...')
    db = FinancialRepository(finance_database_url)
    symbols = ["IBM", "AAPL"]

    try:
        for symbol in symbols:
            finance_api_client = AlphavantageClient(finance_api_client_api_key=finance_api_client_api_key,
                                                    finance_api_client_api_url=finance_api_client_api_url)
            raw_data = finance_api_client.get_raw_data(symbol)
            logger.info(f'Successfully Retrieved RAW Data for {symbol} ...')
            process_data = finance_api_client.process_raw_data(symbol, raw_data, finance_api_client_data_duration)
            db.add_financial_data(process_data)
            logger.info(f'Successfully Stored Processed Finance Data for {symbol} ...')
        logger.info(f'Complete Migration of RAW Data From Finance API to Database...')
    except ApiClientError as e:
        logger.error(f'Failed to Get RAW Data From API... Error:{e}')
    except SQLAlchemyError as e:
        logger.error(f"Failed to insert data into database... Error:{e}")


if __name__ == '__main__':
    main()