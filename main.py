import requests
import json
from datetime import datetime, timedelta
import sqlite3

# Set up API parameters
function = 'TIME_SERIES_DAILY_ADJUSTED'
symbols = ['IBM', 'AAPL']
outputsize = 'compact'
datatype = 'json'
apikey = '2GPIFOE66Y1A7WOP'   # Here you use your API key

# Set up database connection and cursor
conn = sqlite3.connect('financial_data.db')
c = conn.cursor()

# Create financial_data table if it does not exist
try:
    c.execute('''CREATE TABLE financial_data
                 (symbol text, date text, open_price real, close_price real, volume integer)''')
except sqlite3.OperationalError:
    # Table already exists
    pass

# Send API request and process response for each symbol
for symbol in symbols:
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}&datatype={datatype}&apikey={apikey}'

    response = requests.get(url)
    if response.status_code == 200:
        api_data = response.json()['Time Series (Daily)']
        today = datetime.today().strftime('%Y-%m-%d')
        two_weeks_ago = (datetime.today() - timedelta(days=14)).strftime('%Y-%m-%d')
        processed_data = []
        for date, values in api_data.items():
            if date >= two_weeks_ago and date <= today:
                symbol = symbol
                date = date
                open_price = values['1. open']
                close_price = values['4. close']
                volume = values['6. volume']
                processed_data.append({'symbol': symbol, 'date': date, 'open_price': open_price, 'close_price': close_price, 'volume': volume})

        # Insert processed data into database
        for data in processed_data:
            c.execute("INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES (?, ?, ?, ?, ?)", (data['symbol'], data['date'], data['open_price'], data['close_price'], data['volume']))

        # Commit changes
        conn.commit()

        # Print processed data
        print(f"Processed data for {symbol}:")
        print(json.dumps(processed_data, indent=4))
    else:
        print(f'Error: API request for {symbol} unsuccessful.')

# Close connection
conn.close()