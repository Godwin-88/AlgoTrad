#!/usr/bin/python
# -*- coding: utf-8 -*-

# ib_execution.py

import datetime
import time
from ib_insync import IB, Stock, MarketOrder, LimitOrder, Contract, Order, Trade

from event import FillEvent, OrderEvent
from execution import ExecutionHandler


class IBExecutionHandler(ExecutionHandler):
    """
    Handles order execution via the Interactive Brokers
    API, for use against accounts when trading live
    directly.
    """

    def __init__(self, events, order_routing: str = "SMART", currency: str = "USD"):
        """
        Initializes the IBExecutionHandler instance.

        Parameters:
        events - The Queue of Event objects.
        order_routing - The order routing strategy (default "SMART").
        currency - The currency for the orders (default "USD").
        """
        self.events = events
        self.order_routing = order_routing
        self.currency = currency
        self.fill_dict = {}

        self.ib = self.create_ib_connection()
        self.order_id = self.create_initial_order_id()

    def create_ib_connection(self) -> IB:
        """
        Connect to the Trader Workstation (TWS) running on the
        usual port of 7497, with a clientId of 1.
        """
        ib = IB()
        ib.connect('127.0.0.1', 7497, clientId=1)  # Adjust port and clientId as necessary
        return ib

    def create_initial_order_id(self) -> int:
        """
        Creates the initial order ID used for Interactive
        Brokers to keep track of submitted orders.
        """
        # The order ID management is handled by the IB API itself in ib_insync.
        return 1  # Placeholder, not strictly necessary with ib_insync.

    def create_contract(self, symbol: str, sec_type: str, exch: str, prim_exch: str, curr: str) -> Contract:
        """Create a Contract object defining what will be purchased, at which exchange, and in which currency."""
        contract = Stock(symbol, exchange=exch, currency=curr)
        return contract

    def create_order(self, order_type: str, quantity: int, action: str) -> Order:
        """Create an Order object (Market/Limit) to go long/short."""
        if order_type == 'MKT':
            order = MarketOrder(action, quantity)
        elif order_type == 'LMT':
            order = LimitOrder(action, quantity, 0)  # Placeholder for price, adjust as needed
        else:
            raise ValueError(f"Order type {order_type} not supported")
        return order

    def create_fill(self, trade: Trade) -> None:
        """
        Handles the creation of the FillEvent that will be
        placed onto the events queue subsequent to an order
        being filled.
        """
        symbol = trade.contract.symbol
        exchange = trade.contract.exchange
        filled = trade.filled
        direction = trade.order.action
        fill_cost = trade.avgFillPrice

        # Create a fill event object
        fill_event = FillEvent(
            datetime.datetime.utcnow(), symbol,
            exchange, filled, direction, fill_cost
        )

        # Place the fill event onto the event queue
        self.events.put(fill_event)

    def execute_order(self, event: OrderEvent) -> None:
        """
        Creates the necessary InteractiveBrokers order object
        and submits it to IB via their API.

        The results are then queried to generate a
        corresponding Fill object, which is placed back on
        the event queue.

        Parameters:
        event - Contains an Event object with order information.
        """
        if event.type == 'ORDER':
            # Prepare the parameters for the asset order
            asset = event.symbol
            asset_type = "STK"
            order_type = event.order_type
            quantity = event.quantity
            direction = event.direction

            # Create the Interactive Brokers contract via the passed Order event
            ib_contract = self.create_contract(
                asset, asset_type, self.order_routing, self.order_routing, self.currency
            )

            # Create the Interactive Brokers order via the passed Order event
            ib_order = self.create_order(order_type, quantity, direction)

            # Use the connection to send the order to IB
            trade = self.ib.placeOrder(ib_contract, ib_order)

            # Wait for the order to be filled and process the fill
            while not trade.isDone():
                self.ib.sleep(1)

            # Process the fill
            self.create_fill(trade)
