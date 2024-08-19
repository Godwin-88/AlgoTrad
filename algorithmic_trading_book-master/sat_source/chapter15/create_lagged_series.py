#!/usr/bin/python
# -*- coding: utf-8 -*-

# create_lagged_series.py

import pandas as pd
import yfinance as yf

def create_lagged_series(symbol, start_date, end_date, lags=5):
    """
    This creates a DataFrame that stores the percentage returns of the
    adjusted closing value of a stock obtained from Yahoo Finance, along with
    a number of lagged returns from previous trading days (lags defaults to 5 days).
    
    Parameters:
    symbol - A stock symbol (ticker) that the strategy will trade.
    start_date - The start date of the data series.
    end_date - The end date of the data series.
    lags - The number of days to lag the series.
    """

    # Fetch the adjusted closing prices from Yahoo Finance
    ts = yf.download(symbol, start=start_date, end=end_date)

    # Create the new lagged DataFrame
    tslag = pd.DataFrame(index=ts.index)
    tslag["Today"] = ts["Adj Close"]
    
    # Create the shifted lag series of prior trading period close values
    for i in range(0, lags):
        tslag[f"Lag{i+1}"] = ts["Adj Close"].shift(i+1)

    # Create the returns DataFrame
    tsret = pd.DataFrame(index=tslag.index)
    tsret["Today"] = tslag["Today"].pct_change()*100.0
    
    # If any of the values of percentage returns equal zero, set them to a small number
    for i, x in tsret["Today"].items():
        if abs(x) < 1e-10:
            tsret.at[i, "Today"] = 0.0001
    
    # Create the lagged percentage returns columns
    for i in range(0, lags):
        tsret[f"Lag{i+1}"] = tslag[f"Lag{i+1}"].pct_change()*100.0
    
    # Create the "Direction" column (+1 or -1) indicating an up/down day
    tsret["Direction"] = pd.Series([1 if x > 0 else -1 for x in tsret["Today"]], index=tsret.index)
    
    return tsret.dropna()
