#!/usr/bin/python
# -*- coding: utf-8 -*-

# event.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class Event:
    """
    Base class providing an interface for all subsequent 
    (inherited) events that will trigger further events in the 
    trading infrastructure.
    """
    pass


@dataclass
class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with 
    corresponding bars.
    """
    type: str = 'MARKET'


@dataclass
class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """
    strategy_id: int
    symbol: str
    datetime: datetime
    signal_type: str
    strength: float
    type: str = 'SIGNAL'


@dataclass
class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    quantity, and a direction.
    """
    symbol: str
    order_type: str
    quantity: int
    direction: str
    type: str = 'ORDER'

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("Quantity must be non-negative")

    def print_order(self):
        """
        Outputs the values within the Order.
        """
        print(
            f"Order: Symbol={self.symbol}, Type={self.order_type}, "
            f"Quantity={self.quantity}, Direction={self.direction}"
        )


@dataclass
class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from a brokerage. Stores the quantity of an instrument
    actually filled and at what price. In addition, stores
    the commission of the trade from the brokerage.
    """
    timeindex: datetime
    symbol: str
    exchange: str
    quantity: int
    direction: str
    fill_cost: float
    commission: Optional[float] = None
    type: str = 'FILL'

    def __post_init__(self):
        if self.commission is None:
            self.commission = self.calculate_ib_commission()

    def calculate_ib_commission(self) -> float:
        """
        Calculates the fees of trading based on an Interactive
        Brokers fee structure for API, in USD.

        This does not include exchange or ECN fees.

        Based on "US API Directed Orders":
        https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2
        """
        if self.quantity <= 500:
            return max(1.3, 0.013 * self.quantity)
        else:
            return max(1.3, 0.008 * self.quantity)
