from datetime import date

import yfinance as yf

from utils.datasystem.base import DataSystem

data_system = DataSystem()

tickers = [
    "XOM",  # Exxon
    "JNJ",  # Johnson & Johnson
    "WMT",  # Walmart
    "OYST",  # Oyster Point Pharma
]
today = date.today()


def fetch_price_data(**kwargs):
    time_format = today.strftime("%d-%m-%Y")
    for ticker in tickers:
        item = yf.Ticker(ticker)
        pricing_data_historical = item.history(period="1d", interval="1m")

        data_system.put_object(
            "raw-data",
            f"stocks/{ticker}_{today}.csv",
            pricing_data_historical,
            index=True,
        )
