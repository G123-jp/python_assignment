import requests

from clients import FinanceApiClient
from errors import ApiClientError
from config import Config
from common import constants
from schemas import FinancialData


class AlphavantageClient(FinanceApiClient):

    def get_raw_data(self, symbol):
        if Config.finance_api_client_api_key is None:
            raise ApiClientError(f"Missing API KEY.")

        params = {
            "function": constants.API_CLIENT_FUNCTION,
            "symbol": symbol,
            "outputsize": constants.API_CLIENT_OUTPUT_SIZE,
            "apikey": Config.finance_api_client_api_key,
        }

        try:
            response = requests.get(Config.finance_api_client_api_url, params=params)
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
