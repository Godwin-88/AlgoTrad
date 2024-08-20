#!/usr/bin/python
# -*- coding: utf-8 -*-

# hft_data.py

import os
import queue  # Import the queue module
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from event import MarketEvent
from data import DataHandler

class HistoricCSVDataHandlerHFT(DataHandler):
    """
    HistoricCSVDataHandlerHFT is designed to read CSV files for
    each requested symbol from disk and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface.

    This particular class uses DTN IQFeed as its data source.
    """

    def __init__(self, events: queue.Queue, csv_dir: str, symbol_list: List[str]):
        """
        Initializes the historic data handler by requesting
        the location of the CSV files and a list of symbols.

        Parameters:
        events - The Event Queue.
        csv_dir - Absolute directory path to the CSV files.
        symbol_list - A list of symbol strings.
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data: Dict[str, pd.DataFrame] = {}
        self.latest_symbol_data: Dict[str, List[Tuple[pd.Timestamp, pd.Series]]] = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def _open_convert_csv_files(self) -> None:
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.

        For this handler, it will be assumed that the data is
        taken from Yahoo. Thus its format will be respected.
        """
        comb_index = None
        for symbol in self.symbol_list:
            df = pd.read_csv(
                os.path.join(self.csv_dir, f'{symbol}.csv'),
                header=0, index_col=0, parse_dates=True,
                names=['datetime', 'open', 'low', 'high', 'close', 'volume', 'oi']
            ).sort_index()

            if comb_index is None:
                comb_index = df.index
            else:
                comb_index = comb_index.union(df.index)

            self.symbol_data[symbol] = df
            self.latest_symbol_data[symbol] = []

        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=comb_index, method='pad')
            self.symbol_data[symbol]['returns'] = self.symbol_data[symbol]['close'].pct_change()
            self.symbol_data[symbol] = self.symbol_data[symbol].iterrows()

    def _get_new_bar(self, symbol: str):
        """
        Returns the latest bar from the data feed.
        """
        return next(self.symbol_data[symbol])

    def get_latest_bar(self, symbol: str) -> Tuple[pd.Timestamp, pd.Series]:
        """
        Returns the last bar from the latest_symbol list.
        """
        try:
            return self.latest_symbol_data[symbol][-1]
        except IndexError:
            raise ValueError(f"Symbol {symbol} is not available in the historical data set.")

    def get_latest_bars(self, symbol: str, N: int = 1) -> List[Tuple[pd.Timestamp, pd.Series]]:
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            return self.latest_symbol_data[symbol][-N:]
        except IndexError:
            raise ValueError(f"Symbol {symbol} is not available in the historical data set.")

    def get_latest_bar_datetime(self, symbol: str) -> pd.Timestamp:
        """
        Returns a Python datetime object for the last bar.
        """
        return self.get_latest_bar(symbol)[0]

    def get_latest_bar_value(self, symbol: str, val_type: str):
        """
        Returns one of the Open, High, Low, Close, Volume, or OI
        values from the pandas Bar series object.
        """
        return self.get_latest_bar(symbol)[1][val_type]

    def get_latest_bars_values(self, symbol: str, val_type: str, N: int = 1) -> np.ndarray:
        """
        Returns the last N bar values from the 
        latest_symbol list, or N-k if less available.
        """
        bars = self.get_latest_bars(symbol, N)
        return np.array([bar[1][val_type] for bar in bars])

    def update_bars(self) -> None:
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            try:
                bar = self._get_new_bar(symbol)
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())
