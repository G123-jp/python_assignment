import os
from datetime import datetime, timedelta
from decimal import Decimal

import requests
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert as pg_upsert

from financial.model import FinancialData

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.environ["ALPHA_VANTAGE_API_KEY"]
DATABASE_URI = os.environ["DATABASE_URI"]

db = SQLAlchemy()
engine = db.create_engine(DATABASE_URI)
Session = db.sessionmaker(bind=engine)
session = Session()

# Define the function for fetching data from the Alpha Vantage API


def fetch_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=compact&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    return response.json()


# Define the function for parsing the data


def parse_data(raw_data):
    parsed_data = []
    for raw_date, values in raw_data.items():
        date = datetime.strptime(raw_date, "%Y-%m-%d")
        if datetime.now() - date > timedelta(days=14):
            break
        open_price = Decimal(values["1. open"])
        close_price = Decimal(values["4. close"])
        volume = int(values["6. volume"])
        parsed_data.append((date.date(), open_price, close_price, volume))
    return parsed_data


# Define the function for storing the data


def fetch_and_store_data(symbol):
    raw_data = fetch_data(symbol)["Time Series (Daily)"]
    parsed_data = parse_data(raw_data)
    upsert_data = [
        {
            "symbol": symbol,
            "open_price": open_price,
            "close_price": close_price,
            "volume": volume,
            "date": date,
        }
        for date, open_price, close_price, volume in parsed_data
    ]
    financial_data_upsert = (
        db.dialects.postgresql.insert(FinancialData)
        .values(upsert_data)
        .on_conflict_do_nothing(
            index_elements=["symbol", "date"],
        )
    )

    session.execute(financial_data_upsert)
    session.commit()


# Set the parameters for fetching the data
symbols = ["AAPL", "IBM"]

# Fetch and store the data
for symbol in symbols:
    fetch_and_store_data(symbol)
