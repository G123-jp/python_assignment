import os
import requests
from financial import models
from datetime import datetime

from financial.database import SessionLocal, engine
from financial.models import Base

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
ALPHAVANTAGE_API_URL = os.getenv("ALPHAVANTAGE_API_URL")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
Base.metadata.create_all(bind=engine)


def get_raw_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": ALPHAVANTAGE_API_KEY,
    }
    response = requests.get(ALPHAVANTAGE_API_URL, params=params)
    raw_data = response.json()
    return raw_data


def process_raw_data(symbol, raw_data):
    time_series = raw_data.get("Time Series (Daily)", {})
    financial_data = []
    for date_str, values in time_series.items():
        if (datetime.today() - datetime.strptime(date_str, "%Y-%m-%d")).days > 14:
            continue
        date = datetime.strptime(date_str, "%Y-%m-%d")
        open_price = values.get("1. open")
        close_price = values.get("4. close")
        volume = values.get("6. volume")
        financial_data.append(models.FinancialData(symbol=symbol, date=date, open_price=open_price,
                                                   close_price=close_price, volume=volume))
    return financial_data


def save_financial_data(financial_data, session):
    session.add_all(financial_data)
    session.commit()


def main():
    session = SessionLocal()
    symbols = ["IBM", "AAPL"]
    for symbol in symbols:
        raw_data = get_raw_data(symbol)
        financial_data = process_raw_data(symbol, raw_data)
        save_financial_data(financial_data, session)


if __name__ == '__main__':
    main()
