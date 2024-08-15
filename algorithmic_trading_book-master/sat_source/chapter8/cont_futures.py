#!/usr/bin/python
# -*- coding: utf-8 -*-

# cont_futures.py
import datetime
import numpy as np
import pandas as pd
import quandl

def futures_rollover_weights(start_date, expiry_dates, contracts, rollover_days=5):
    """
    Constructs a pandas DataFrame containing weights (between 0.0 and 1.0)
    of contract positions to hold in order to carry out a rollover of rollover_days
    prior to the expiration of the earliest contract. The matrix can then be
    'multiplied' with another DataFrame containing the settle prices of each
    contract to produce a continuous time series futures contract.
    """
    # Construct a sequence of dates from the start date to the last expiry date
    dates = pd.date_range(start_date, expiry_dates.iloc[-1], freq='B')

    # Create the roll weights DataFrame
    roll_weights = pd.DataFrame(np.zeros((len(dates), len(contracts))),
                                index=dates, columns=contracts)
    prev_date = roll_weights.index[0]

    # Loop through each contract to create specific weightings
    for i, (item, ex_date) in enumerate(expiry_dates.iteritems()):
        if i < len(expiry_dates) - 1:
            roll_weights.loc[prev_date:ex_date - pd.offsets.BDay(), item] = 1
            roll_rng = pd.date_range(end=ex_date - pd.offsets.BDay(),
                                     periods=rollover_days + 1, freq='B')

            # Create a sequence of roll weights and adjust the weightings
            decay_weights = np.linspace(0, 1, rollover_days + 1)
            roll_weights.loc[roll_rng, item] = 1 - decay_weights
            roll_weights.loc[roll_rng, expiry_dates.index[i+1]] = decay_weights
        else:
            roll_weights.loc[prev_date:, item] = 1
        prev_date = ex_date
    return roll_weights

if __name__ == "__main__":
    # Set your Quandl API key (if you have one)
    quandl.ApiConfig.api_key = 'your_api_key_here'

    # Download the current Front and Back (near and far) futures contracts for WTI Crude from Quandl
    wti_near = quandl.get("OFDP/FUTURE_CLF2014")
    wti_far = quandl.get("OFDP/FUTURE_CLG2014")
    wti = pd.DataFrame({'CLF2014': wti_near['Settle'],
                        'CLG2014': wti_far['Settle']}, index=wti_far.index)

    # Create the dictionary of expiry dates for each contract
    expiry_dates = pd.Series({'CLF2014': datetime.datetime(2013, 12, 19),
                              'CLG2014': datetime.datetime(2014, 2, 21)}).sort_values()

    # Obtain the rollover weighting matrix/DataFrame
    weights = futures_rollover_weights(wti_near.index[0], expiry_dates, wti.columns)

    # Construct the continuous future of the WTI CL contracts
    wti_cts = (wti * weights).sum(axis=1).dropna()

    # Output the merged series of contract settle prices
    print(wti_cts.tail(60))
