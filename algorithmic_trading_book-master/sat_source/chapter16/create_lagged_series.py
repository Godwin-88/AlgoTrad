#!/usr/bin/python
# -*- coding: utf-8 -*-

# create_lagged_series.py

import datetime
import numpy as np
import pandas as pd
import yfinance as yf


def create_lagged_series(symbol: str, start_date: datetime.datetime, end_date: datetime.datetime, lags: int = 5) -> pd.DataFrame:
    """
    This creates a pandas DataFrame that stores the percentage returns of the adjusted closing value of a stock obtained
    from Yahoo Finance, along with a number of lagged returns from the prior trading days (lags defaults to 5 days).
    Trading volume, as well as the Direction from the previous day, are also included.

    Parameters:
    - symbol: The ticker symbol of the stock.
    - start_date: The start date for retrieving data.
    - end_date: The end date for retrieving data.
    - lags: The number of lagged periods to include.

    Returns:
    - tsret: A DataFrame with the lagged series and additional columns.
    """

    # Obtain stock information from Yahoo Finance
    ts = yf.download(symbol, start=start_date - datetime.timedelta(days=365), end=end_date)

    # Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslag["Today"] = ts["Adj Close"]
    tslag["Volume"] = ts["Volume"]

    # Create the shifted lag series of prior trading period close values
    for i in range(1, lags + 1):
        tslag[f"Lag{i}"] = ts["Adj Close"].shift(i)

    # Create the returns DataFrame
    tsret = pd.DataFrame(index=tslag.index)
    tsret["Volume"] = tslag["Volume"]
    tsret["Today"] = tslag["Today"].pct_change() * 100.0

    # If any of the values of percentage returns equal zero, set them to a small number
    tsret["Today"].replace(0, 0.0001, inplace=True)

    # Create the lagged percentage returns columns
    for i in range(1, lags + 1):
        tsret[f"Lag{i}"] = tslag[f"Lag{i}"].pct_change() * 100.0

    # Create the "Direction" column (+1 or -1) indicating an up/down day
    tsret["Direction"] = np.sign(tsret["Today"])
    tsret = tsret[tsret.index >= start_date]

    return tsret
