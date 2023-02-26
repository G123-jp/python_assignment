import json
import os,requests
from datetime import datetime, timedelta
from model import FinancialData
from dotenv import load_dotenv
from utilities import StockSymbol, Helpers

class StockDataFetcher():
    # Base URL for the AlphaVantage API
    BASE_URL        = "https://www.alphavantage.co/query"
    CACHE_FILENAME  = 'cached_data.json'

    def __init__(self,api_key,symbols):
        self.__api_key        = api_key
        self.symbols          = symbols
        self.__cached_data    = self.__load_cached_data()
        self.__new_data       = []
        # Set the date variables for the 2 weeks date range
        self.date_today       = datetime.today().strftime("%Y-%m-%d")
        self.date_2weeks_ago  = (datetime.today() - timedelta(days=14)).strftime("%Y-%m-%d")

    # PRIVATE METHODS
    def __load_cached_data(self):
        """
        Loads cached data from the 'cached_data.json' file, if it exists.

        Returns:
        cached_data: A list of cached data from the 'cached_data.json' file, if it exists.
                     If the file does not exist, an empty list is returned.
        """
        cached_data = []
        # Read the cached_data from 'cached_data.json'
        if os.path.isfile(self.CACHE_FILENAME):
            with open(self.CACHE_FILENAME, 'r') as f:
                cached_data = json.load(f)
        return cached_data

    def __save_cached_data(self,new_data):
        """
        Save the newly retrieved financial data to the cache file 'cached_data.json'.
        This method overwrites the cached data with the new data and writes the updated data to the file.

        Args:
            new_data (list): The new financial data to be cached.
        """
        # Overwrite cached_data with the newly retrieved financial data
        self.__cached_data = new_data
        # Write the new cached_data in 'cached_data.json'
        with open(self.CACHE_FILENAME, 'w') as f:
            json.dump(self.__cached_data, f)

    def __retrieve_api_data(self):
        """
        Retrieve API Data

        Retrieves data from AlphaVantage's open API.
        API Documentation -> https://www.alphavantage.co/documentation/
        """
        raw_data = {}
        for symbol in self.symbols:
            # Define the parameters for the API request
            params = {
                "function"      : "TIME_SERIES_DAILY_ADJUSTED",
                "symbol"        : symbol,
                "outputsize"    : "compact",
                "apikey"        : self.__api_key,
            }
            try:
                # Make the API request and retrieve the response
                response = requests.get(self.BASE_URL, params)
                response.raise_for_status()  # raise an HTTPError for 4xx and 5xx status codes
                data = response.json()["Time Series (Daily)"]
                raw_data[symbol] = data
            except requests.exceptions.RequestException as ex:
                Helpers.print_text(f"Failed to retrieve data for symbol {symbol}. Error: {ex}", error=True)

        return raw_data

    def __process_data(self,raw_data):
        """
        Process the raw financial data retrieved from the API and return a list of financial
        data dictionaries,filtered to include only the most recent 2 weeks of data.

        Args:
            raw_data (dict): The raw financial data retrieved from the API, in the format of a
                             nested dictionary with symbols as keys and date-value pairs as values.

        Returns:
            list: A list of financial data dictionaries, each containing the following keys:
                  'symbol', 'date', 'open_price', 'close_price', and 'volume'.

                  The list is filtered to only include data from the most recent 2 weeks and
                  exclude any duplicates already present in the cached data. If new data is found,
                  it is added to the new_data list.
        """
        financial_data_list = []
        for symbol,data in raw_data.items():
            for date_str, values in data.items():
                date = datetime.strptime(date_str, "%Y-%m-%d")

                # Filter the data to get the most recent 2 weeks
                if date >= datetime.strptime(self.date_2weeks_ago, "%Y-%m-%d") and date <= datetime.strptime(self.date_today, "%Y-%m-%d"):
                    financial_data_list.append({
                        "symbol"        : symbol,
                        "date"          : date_str,
                        "open_price"    : values["1. open"],
                        "close_price"   : values["4. close"],
                        "volume"        : values["6. volume"]
                    })

        # Add the newly retrieved financial data in new_data dictionary if it doesn't exist in the cached_data
        for financial_data in financial_data_list:
            if financial_data not in self.__cached_data:
                self.__new_data.append(financial_data)

        return financial_data_list

    # PUBLIC METHODS
    def get_data(self):
        """
        Retrieve stock data

        Check if stock data for as of the last stock market date is present in the cached data:

        if YES: Return the cached data. Caching data can help to improve the performance,
                reliability, and cost-effectiveness of the application when making API calls
        if NO: Get the new data from the API and return it
        """

        # If date_today falls on weekends, get the date of the last weekday(friday)
        # since stock markets are closed during weekends
        today = datetime.today()
        if today.weekday() == 5:  # Saturday
            last_stock_date = today - timedelta(days=1)
        elif today.weekday() == 6:  # Sunday
            last_stock_date = today - timedelta(days=2)
        else:
            last_stock_date = today

        # Check the cached data if last_stock_date data is existing
        if any(data["date"] == last_stock_date.strftime("%Y-%m-%d") for data in self.__cached_data):
            Helpers.print_text("[Get Data] Data retrieved from cached data.")
            return self.__cached_data

        # Get the data from API and process it
        raw_api_data        = self.__retrieve_api_data()
        financial_data_list = self.__process_data(raw_api_data)
        # Cache the newly retrieved data
        self.__save_cached_data(financial_data_list)

        Helpers.print_text("[Get Data] Data retrieved from API")
        return financial_data_list

    def save_financial_data(self):
        """
        Save Financial Data

        Inserts new financial data to the database if it doesn't already exist. Skips data if it is already
        present in the database. If no new data is retrieved, prints a message stating there is no new data.
        """
        try:
            # Bail out early if no new data retrieved
            if len(self.__new_data) == 0:
                Helpers.print_text("[Insert Data] No new data.",True)
                return

            for financial_data in self.__new_data:
                symbol  = financial_data["symbol"]
                date    = financial_data["date"]

                # Check if data already exists using the data's symbol and date
                existing_data = FinancialData.select().where(
                    (FinancialData.symbol == symbol) & (FinancialData.date == date)
                )

                # Skip duplicate data
                if existing_data.exists():
                    # display duplicate message
                    Helpers.print_text(f"[Insert Data] Skipped: {symbol} data for date [{date}] already exists",True)
                    continue

                # Insert new data into the database
                data = FinancialData(
                    symbol      = symbol,
                    date        = date,
                    open_price  = financial_data["open_price"],
                    close_price = financial_data["close_price"],
                    volume      = financial_data["volume"]
                )
                data.save()
                Helpers.print_text(f"[Insert Data] Added: {symbol} data for date [{date}]")

            # Clear new_data container
            self.__new_data.clear()
        except Exception as ex:
            Helpers.print_text(Helpers.get_root_cause(ex),True)

def main():
    # Load environment variables including the .env file
    # in the project root folder containing the API KEY
    load_dotenv()
    api_key = os.environ.get('API_KEY')
    if api_key is None:
        Helpers.print_text("API_KEY environment variable not set",True)
        return

    # We will be retrieving stock data for Apple and IBM.
    symbols = [StockSymbol.Apple.value,StockSymbol.IBM.value]

    data_fetcher = StockDataFetcher(api_key,symbols)
    raw_data = data_fetcher.get_data()
    print("\n%s\n" % raw_data)
    data_fetcher.save_financial_data()

if __name__ == "__main__":
    main()