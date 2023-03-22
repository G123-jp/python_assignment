import argparse
import grequests
import psycopg

class StockPriceEntry:

    def __init__(self, symbol, date, rawData):
        self.symbol = symbol
        self.date = date

        for key, value in rawData.items():
            if "open" in key.lower():
                self.openPrice = value
            elif "close" in key.lower():
                self.closePrice = value
            elif "volume" in key.lower():
                self.volume = value

    def GetDictFormat(self):
        return {
            "symbol": self.symbol,
            "date": self.date,
            "open_price": self.openPrice,
            "close_price": self.closePrice,
            "volume": self.volume,
        }        

    def GetTupleFormat(self):
        return (
            self.symbol,
            self.date,
            self.openPrice,
            self.closePrice,
            self.volume,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbols', dest='symbols', type=str, nargs=2, required=True, help="Stock symbols, requires exactly two stock symbols")
    parser.add_argument('--apikey', dest='apiKey', type=str, required=True, help="Api key for retrieving financial data")
    parser.add_argument('--numDays', dest='numDays', type=int, default=14, help="Number of days (database entries) for stock prices")
    args = parser.parse_args()
    
    urls = ["https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={apiKey}".format(symbol=symbol.upper(), apiKey=args.apiKey) for symbol in args.symbols]
    results = grequests.map(grequests.get(u) for u in urls)

    formattedData = []
    for r in results:
        data = r.json()

        symbol = data.get('Meta Data').get('2. Symbol')
        timeSeriesData = data.get('Time Series (Daily)')

        for date in list(timeSeriesData.keys())[0:args.numDays]:
            formattedData.append(StockPriceEntry(symbol, date, timeSeriesData.get(date)).GetTupleFormat())

    with psycopg.connect('host=localhost port=5432 user=shaysrebellion password=webserverdb dbname=stocks') as conn:
        with conn.cursor() as cursor:
            # pyscopg3's implementation of executemany is supposed to be substantially faster than that in psycopg2:
            # executemany is faster than sequentially (individually) inserting rows into the (postgres) database
            # Should INSERT writes scale (larger writes and/or more frequent writes), then psycopg3's binary copy
            # can be considered: https://www.psycopg.org/psycopg3/docs/basic/copy.html#binary-copy
            cursor.executemany(
                """
                INSERT INTO financial_data VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                formattedData
            )
            conn.commit()


if __name__ == "__main__":
    main()
