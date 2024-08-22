import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the stock symbols for tech, banking, and other assets
tech_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "ORCL", "INTC", "ADBE"]
banking_stocks = ["JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC", "TFC", "BK"]
other_assets = ["GC=F", "SI=F", "CL=F", "BTC-USD", "ETH-USD", "EURUSD=X", "JPY=X", "GBPUSD=X", "USO", "GLD"]

# Combine all symbols into one list
all_symbols = tech_stocks + banking_stocks + other_assets

# Define the date range
start_date = "1990-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

# Function to download data and save as CSV
def download_and_save_data(symbol):
    try:
        # Download the data
        data = yf.download(symbol, start=start_date, end=end_date)
        # Save the data to a CSV file named after the symbol
        data.to_csv(f"{symbol}.csv")
        print(f"Downloaded and saved {symbol}.csv")
    except Exception as e:
        print(f"Failed to download {symbol}: {e}")

# Download and save data for each symbol
for symbol in all_symbols:
    download_and_save_data(symbol)

