#!/usr/bin/python
# -*- coding: utf-8 -*-

# data.py

from abc import ABC, abstractmethod
from datetime import datetime
import os
from typing import List, Dict, Tuple, Iterator

import numpy as np
import pandas as pd

from event import MarketEvent
import pandas as pd

from event import MarketEvent


class DataHandler(ABC):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).
    """

    @abstractmethod
    def get_latest_bar(self, symbol: str):
        raise NotImplementedError("Should implement get_latest_bar()")

    @abstractmethod
    def get_latest_bars(self, symbol: str, N: int = 1):
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol: str):
        raise NotImplementedError("Should implement get_latest_bar_datetime()")

    @abstractmethod
    def get_latest_bar_value(self, symbol: str, val_type: str):
        raise NotImplementedError("Should implement get_latest_bar_value()")

    @abstractmethod
    def get_latest_bars_values(self, symbol: str, val_type: str, N: int = 1):
        raise NotImplementedError("Should implement get_latest_bars_values()")

    @abstractmethod
    def update_bars(self):
        raise NotImplementedError("Should implement update_bars()")


class HistoricCSVDataHandler(DataHandler):
    """
    HistoricCSVDataHandler is designed to read CSV files for
    each requested symbol from disk and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface.
    """

    def __init__(self, events, csv_dir, symbol_list):
        """
        Initializes the historic data handler by requesting
        the location of the CSV files and a list of symbols.

        Parameters:
        events - The Event Queue.
        csv_dir - The directory where CSV files are stored.
        symbol_list - A list of symbol strings.
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self.bar_index = 0

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.
        """
        comb_index = None
        for symbol in self.symbol_list:
            df = pd.read_csv(
                os.path.join(self.csv_dir, f'{symbol}.csv'),
                header=0, index_col=0, parse_dates=True
            ).sort_index()

            # Create the 'returns' column based on 'adj_close'
            df['returns'] = df['adj_close'].pct_change()

            # Store the DataFrame in the symbol dictionary
            self.symbol_data[symbol] = df

            # Ensure the index for the DataFrame is properly aligned
            if comb_index is None:
                comb_index = df.index
            else:
                comb_index = comb_index.union(df.index)

            self.latest_symbol_data[symbol] = []

        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=comb_index, method='pad')
            self.symbol_data[symbol] = self.symbol_data[symbol].iterrows()

    def get_latest_bar(self, symbol: str):
        """
        Returns the last bar from the latest_symbol list.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            raise KeyError(f"Symbol {symbol} is not available in the data set.")
        return bars_list[-1]

    def get_latest_bars(self, symbol: str, N: int = 1):
        """
        Returns the last N bars from the latest_symbol list.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            raise KeyError(f"Symbol {symbol} is not available in the data set.")
        return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol: str):
        """
        Returns a Python datetime object for the last bar.
        """
        bar = self.get_latest_bar(symbol)
        return bar[0]  # The first element of the tuple is the datetime index

    def get_latest_bar_value(self, symbol, val_type):
        """
        Returns one of the Open, High, Low, Close, Volume, or Adj Close
        from the pandas Bar series object.
        """
        bar = self.get_latest_bar(symbol)  # `get_latest_bar` should return a tuple (index, Series)
        return bar[1][val_type]  # Access the desired column in the Series

    
    def get_latest_bars_values(self, symbol: str, val_type: str, N: int = 1):
        """
        Returns the last N bar values from the latest_symbol list, or N-k if less available.
        """
        bars = self.get_latest_bars(symbol, N)
        # Access the second element of the tuple, which is the row data (a Series)
        return [getattr(bar[1], val_type) for bar in bars]


    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            try:
                bar = next(self.symbol_data[symbol])  # Fetch the next bar tuple (index, Series)
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())
