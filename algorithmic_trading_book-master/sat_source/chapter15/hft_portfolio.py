#!/usr/bin/python
# -*- coding: utf-8 -*-

# portfolio.py

import datetime
import queue
from math import floor
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

from event import FillEvent, OrderEvent, SignalEvent
from performance import create_sharpe_ratio, create_drawdowns


class PortfolioHFT:
    """
    The Portfolio class handles the positions and market
    value of all instruments at a resolution of one
    minutely bar. It is almost identical to the standard
    Portfolio class, except that the Sharpe Ratio 
    calculation is modified and the correct call is made
    to the HFT Data object for the 'close' price with 
    DTN IQFeed data.

    The positions DataFrame stores a time-index of the 
    quantity of positions held. 

    The holdings DataFrame stores the cash and total market
    holdings value of each symbol for a particular 
    time-index, as well as the percentage change in 
    portfolio total across bars.
    """

    def __init__(self, bars, events: queue.Queue, start_date: datetime.datetime, initial_capital: float = 100000.0):
        """
        Initializes the portfolio with bars and an event queue. 
        Also includes a starting datetime index and initial capital 
        (USD unless otherwise stated).

        Parameters:
        bars - The DataHandler object with current market data.
        events - The Event Queue object.
        start_date - The start date (bar) of the portfolio.
        initial_capital - The starting capital in USD.
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital

        self.all_positions = self.construct_all_positions()
        self.current_positions = {symbol: 0 for symbol in self.symbol_list}

        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()

    def construct_all_positions(self) -> List[Dict[str, float]]:
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        positions = {symbol: 0 for symbol in self.symbol_list}
        positions['datetime'] = self.start_date
        return [positions]

    def construct_all_holdings(self) -> List[Dict[str, float]]:
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        holdings = {symbol: 0.0 for symbol in self.symbol_list}
        holdings['datetime'] = self.start_date
        holdings['cash'] = self.initial_capital
        holdings['commission'] = 0.0
        holdings['total'] = self.initial_capital
        return [holdings]

    def construct_current_holdings(self) -> Dict[str, float]:
        """
        Constructs the dictionary which will hold the instantaneous
        value of the portfolio across all symbols.
        """
        current_holdings = {symbol: 0.0 for symbol in self.symbol_list}
        current_holdings['cash'] = self.initial_capital
        current_holdings['commission'] = 0.0
        current_holdings['total'] = self.initial_capital
        return current_holdings

    def update_timeindex(self, event) -> None:
        """
        Adds a new record to the positions matrix for the current 
        market data bar. This reflects the PREVIOUS bar, i.e. all
        current market data at this stage is known (OHLCV).

        Makes use of a MarketEvent from the events queue.
        """
        latest_datetime = self.bars.get_latest_bar_datetime(self.symbol_list[0])

        # Update positions
        positions = {symbol: self.current_positions[symbol] for symbol in self.symbol_list}
        positions['datetime'] = latest_datetime
        self.all_positions.append(positions)

        # Update holdings
        holdings = {symbol: 0.0 for symbol in self.symbol_list}
        holdings['datetime'] = latest_datetime
        holdings['cash'] = self.current_holdings['cash']
        holdings['commission'] = self.current_holdings['commission']
        holdings['total'] = self.current_holdings['cash']

        for symbol in self.symbol_list:
            market_value = self.current_positions[symbol] * self.bars.get_latest_bar_value(symbol, "close")
            holdings[symbol] = market_value
            holdings['total'] += market_value

        self.all_holdings.append(holdings)

    def update_positions_from_fill(self, fill: FillEvent) -> None:
        """
        Takes a Fill object and updates the position matrix to
        reflect the new position.

        Parameters:
        fill - The Fill object to update the positions with.
        """
        fill_dir = 1 if fill.direction == 'BUY' else -1
        self.current_positions[fill.symbol] += fill_dir * fill.quantity

    def update_holdings_from_fill(self, fill: FillEvent) -> None:
        """
        Takes a Fill object and updates the holdings matrix to
        reflect the holdings value.

        Parameters:
        fill - The Fill object to update the holdings with.
        """
        fill_dir = 1 if fill.direction == 'BUY' else -1
        fill_cost = self.bars.get_latest_bar_value(fill.symbol, "close")
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)

    def update_fill(self, event: FillEvent) -> None:
        """
        Updates the portfolio's current positions and holdings 
        from a FillEvent.
        """
        if event.type == 'FILL':
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)

    def generate_naive_order(self, signal: SignalEvent) -> OrderEvent:
        """
        Simply files an Order object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.

        Parameters:
        signal - The SignalEvent containing signal information.
        """
        symbol = signal.symbol
        direction = signal.signal_type

        mkt_quantity = 100
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and cur_quantity == 0:
            return OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
        elif direction == 'SHORT' and cur_quantity == 0:
            return OrderEvent(symbol, order_type, mkt_quantity, 'SELL')
        elif direction == 'EXIT' and cur_quantity > 0:
            return OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')
        elif direction == 'EXIT' and cur_quantity < 0:
            return OrderEvent(symbol, order_type, abs(cur_quantity), 'BUY')
        return None

    def update_signal(self, event: SignalEvent) -> None:
        """
        Acts on a SignalEvent to generate new orders 
        based on the portfolio logic.
        """
        if event.type == 'SIGNAL':
            order_event = self.generate_naive_order(event)
            if order_event:
                self.events.put(order_event)

    def create_equity_curve_dataframe(self) -> None:
        """
        Creates a pandas DataFrame from the all_holdings
        list of dictionaries.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
        self.equity_curve = curve

    def output_summary_stats(self) -> List[Tuple[str, str]]:
        """
        Creates a list of summary statistics for the portfolio.
        """
        total_return = self.equity_curve['equity_curve'].iloc[-1]
        returns = self.equity_curve['returns']
        pnl = self.equity_curve['equity_curve']

        sharpe_ratio = create_sharpe_ratio(returns, periods=252 * 6.5 * 60)
        drawdown, max_dd, dd_duration = create_drawdowns(pnl)
        self.equity_curve['drawdown'] = drawdown

        stats = [
            ("Total Return", f"{(total_return - 1.0) * 100.0:.2f}%"),
            ("Sharpe Ratio", f"{sharpe_ratio:.2f}"),
            ("Max Drawdown", f"{max_dd * 100.0:.2f}%"),
            ("Drawdown Duration", f"{dd_duration}")
        ]

        self.equity_curve.to_csv('equity.csv')
        return stats
