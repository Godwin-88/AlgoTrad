#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py
from __future__ import print_function

import datetime
import warnings
import pymysql
import requests
import yfinance as yf
import pandas as pd

# Database connection details
db_host = 'localhost'
db_user = 'sec_user'
db_pass = '1120'
db_name = 'securities_master'

def obtain_list_of_db_tickers(con):
    """
    Obtains a list of the ticker symbols in the database.
    """
    with con.cursor() as cur: 
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
        return [(d[0], d[1]) for d in data]

def get_daily_historic_data_yahoo(ticker, start_date="2000-01-01"):
    """
    Obtains data from Yahoo Finance using yfinance and returns a DataFrame.

    ticker: Yahoo Finance ticker symbol, e.g., "GOOG" for Google, Inc.
    start_date: Start date in "YYYY-MM-DD" format.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        df = ticker_data.history(start=start_date, end=datetime.date.today().strftime("%Y-%m-%d"))

        # Check if 'Adj Close' is available, otherwise fallback to 'Close'
        if 'Adj Close' not in df.columns:
            print(f"Warning: 'Adj Close' not available for {ticker}. Using 'Close' instead.")
            df['Adj Close'] = df['Close']
        
        df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']]
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        print(f"Could not download Yahoo data for {ticker}: {e}")
        return None

def insert_daily_data_into_db(con, data_vendor_id, symbol_id, daily_data):
    """
    Takes a DataFrame of daily data and adds it to the
    MySQL database. Appends the vendor ID and symbol ID to the data.
    """
    # Create the time now
    now = datetime.datetime.utcnow()

    # Amend the data to include the vendor ID and symbol ID
    daily_data = [
        (data_vendor_id, symbol_id, row['Date'], now, now,
        row['Open'], row['High'], row['Low'], row['Close'], 
        row['Volume'], row['Adj Close']) 
        for index, row in daily_data.iterrows()
    ]

    # Create the insert strings
    column_str = """data_vendor_id, symbol_id, price_date, created_date, 
                 last_updated_date, open_price, high_price, low_price, 
                 close_price, volume, adj_close_price"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % \
        (column_str, insert_str)

    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    try:
        with con.cursor() as cur:
            cur.executemany(final_str, daily_data)
        con.commit()
    except pymysql.MySQLError as e:
        print(f"Error inserting data into the database: {e}")
        con.rollback()

if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation
    warnings.filterwarnings('ignore')

    try:
        # Establish a database connection
        con = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
        print("Connected to the database successfully!")
        
        # Loop over the tickers and insert the daily historical data into the database
        tickers = obtain_list_of_db_tickers(con)
        lentickers = len(tickers)
        for i, t in enumerate(tickers):
            print(f"Adding data for {t[1]}: {i+1} out of {lentickers}")
            yf_data = get_daily_historic_data_yahoo(t[1])
            if yf_data is not None:
                insert_daily_data_into_db(con, '1', t[0], yf_data)
            else:
                print(f"Skipping {t[1]} due to data retrieval failure.")
        print("Successfully added Yahoo Finance pricing data to DB.")

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    
    finally:
        if con and con.open:
            con.close()
            print("Database connection closed.")
