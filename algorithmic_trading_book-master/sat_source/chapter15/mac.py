#!/usr/bin/python
# -*- coding: utf-8 -*-

# mac.py

import datetime
import numpy as np
from typing import Dict, List

from strategy import Strategy
from event import SignalEvent
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio


class MovingAverageCrossStrategy(Strategy):
    """
    Carries out a basic Moving Average Crossover strategy with a
    short/long simple weighted moving average. Default short/long
    windows are 100/400 periods respectively.
    """

    def __init__(
        self, bars: HistoricCSVDataHandler, events: List[SignalEvent], 
        short_window: int = 100, long_window: int = 400
    ):
        """
        Initializes the Moving Average Cross Strategy.

        Parameters:
        bars - The DataHandler object that provides bar information.
        events - The Event Queue object.
        short_window - The short moving average lookback period.
        long_window - The long moving average lookback period.
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        self.short_window = short_window
        self.long_window = long_window

        # Set to True if a symbol is in the market
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self) -> Dict[str, str]:
        """
        Initializes the bought dictionary for all symbols
        and sets them to 'OUT'.
        """
        return {symbol: 'OUT' for symbol in self.symbol_list}

    def calculate_signals(self, event) -> None:
        """
        Generates a new set of signals based on the MAC
        SMA with the short window crossing the long window
        meaning a long entry and vice versa for a short entry.

        Parameters:
        event - A MarketEvent object.
        """
        if event.type == 'MARKET':
            for symbol in self.symbol_list:
                bars = self.bars.get_latest_bars_values(
                    symbol, "adj_close", N=self.long_window
                )
                bar_date = self.bars.get_latest_bar_datetime(symbol)
                
                if bars is not None and len(bars) >= self.long_window:
                    short_sma = np.mean(bars[-self.short_window:])
                    long_sma = np.mean(bars[-self.long_window:])

                    dt = datetime.datetime.utcnow()
                    sig_dir = ""

                    if short_sma > long_sma and self.bought[symbol] == "OUT":
                        print(f"LONG: {bar_date}")
                        sig_dir = 'LONG'
                        signal = SignalEvent(1, symbol, dt, sig_dir, 1.0)
                        self.events.put(signal)
                        self.bought[symbol] = 'LONG'
                    elif short_sma < long_sma and self.bought[symbol] == "LONG":
                        print(f"SHORT: {bar_date}")
                        sig_dir = 'EXIT'
                        signal = SignalEvent(1, symbol, dt, sig_dir, 1.0)
                        self.events.put(signal)
                        self.bought[symbol] = 'OUT'


if __name__ == "__main__":
    csv_dir = '/home/ed/AlgorithmicTrading/algorithmic_trading_book-master/sat_source/chapter15/'  # CHANGE THIS TO YOUR ACTUAL CSV DIRECTORY
    symbol_list = ['AAPL']
    initial_capital = 100000.0
    heartbeat = 0.0
    start_date = datetime.datetime(1990, 1, 1, 0, 0, 0)

    backtest = Backtest(
        csv_dir, symbol_list, initial_capital, heartbeat, 
        start_date, HistoricCSVDataHandler, SimulatedExecutionHandler, 
        Portfolio, MovingAverageCrossStrategy
    )
    backtest.simulate_trading()
