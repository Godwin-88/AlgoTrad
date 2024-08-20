#!/usr/bin/python
# -*- coding: utf-8 -*-

# plot_performance.py

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_equity_curve(data: pd.DataFrame, save_path: str = "performance_plot.png") -> None:
    """
    Plots the equity curve, period returns, and drawdowns.

    Parameters:
    - data: A pandas DataFrame containing 'equity_curve', 'returns', and 'drawdown' columns.
    - save_path: The file path where the plot will be saved.
    """
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    fig.patch.set_facecolor('white')

    # Plot the equity curve
    axes[0].set_ylabel('Portfolio value, %')
    data['equity_curve'].plot(ax=axes[0], color="blue", lw=2)
    axes[0].grid(True)

    # Plot the period returns
    axes[1].set_ylabel('Period returns, %')
    data['returns'].plot(ax=axes[1], color="black", lw=2)
    axes[1].grid(True)

    # Plot the drawdowns
    axes[2].set_ylabel('Drawdowns, %')
    data['drawdown'].plot(ax=axes[2], color="red", lw=2)
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig(save_path)  # Save the figure to a file
    print(f"Plot saved to {save_path}")



def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads the CSV data from the given filepath and returns a DataFrame.

    Parameters:
    - filepath: The path to the CSV file.

    Returns:
    - A pandas DataFrame with the loaded data.
    """
    data = pd.read_csv(filepath, header=0, parse_dates=True, index_col=0)
    data.sort_index(inplace=True)
    return data


if __name__ == "__main__":
    filepath = "equity.csv"  # Ensure this path is correct
    if os.path.exists(filepath):
        data = load_data(filepath)
        plot_equity_curve(data)
    else:
        print(f"File {filepath} does not exist.")
