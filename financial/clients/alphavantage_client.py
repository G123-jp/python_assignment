import requests

from financial.clients.interfaces import FinanceApiClient
from financial.errors import ApiClientError
from financial.config import Config
from financial.common import constants
from financial.schemas.finance import FinancialData


class AlphavantageClient(FinanceApiClient):

    def __init__(self, finance_api_client_api_key: str = Config.finance_api_client_api_key,
                 finance_api_client_api_url: str = Config.finance_api_client_api_url) -> None:
        self.finance_api_client_api_key = finance_api_client_api_key
        self.finance_api_client_api_url = finance_api_client_api_url

    def get_raw_data(self, symbol):
        if self.finance_api_client_api_key is None:
            raise ApiClientError(f"Missing API KEY.")

        params = {
            "function": constants.API_CLIENT_FUNCTION,
            "symbol": symbol,
            "outputsize": constants.API_CLIENT_OUTPUT_SIZE,
            "apikey": self.finance_api_client_api_key,
        }

        try:
            response = requests.get(self.finance_api_client_api_url, params=params)
            response.raise_for_status()
            raw_data = response.json()
            return raw_data
        except ApiClientError:
            raise
        except requests.exceptions.RequestException as e:
            raise ApiClientError(f"Failed to retrieve data from API. Error[{e}]")
        except Exception as e:
            raise ApiClientError(f"Unknown error. Error[{e}]")

    def process_raw_data(self, symbol, raw_data, duration):
        daily_data = raw_data.get(constants.API_CLIENT_TIME_GRANULARITY, {})
        dates = list(daily_data.keys())[:duration]
        dates.reverse()

        process_data = []
        for date in dates:
            daily = daily_data[date]
            open_price = daily.get("1. open")
            close_price = daily.get("4. close")
            volume = daily.get("6. volume")

            process_data.append(
                FinancialData(symbol=symbol, date=date, open_price=open_price, close_price=close_price, volume=volume))
        return process_data
