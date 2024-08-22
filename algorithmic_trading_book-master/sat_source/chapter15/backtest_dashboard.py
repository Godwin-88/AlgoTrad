
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the backtest data
@st.cache
def load_data():
    data = pd.read_csv('equity.csv', parse_dates=True, index_col=0)
    return data

# Plot functions
def plot_equity_curve(data):
    fig, ax = plt.subplots()
    data['equity_curve'].plot(ax=ax, color="blue", lw=2.)
    ax.set_title("Equity Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio value, %")
    st.pyplot(fig)

def plot_returns(data):
    fig, ax = plt.subplots()
    data['returns'].plot(ax=ax, color="black", lw=2.)
    ax.set_title("Period Returns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Returns, %")
    st.pyplot(fig)

def plot_drawdowns(data):
    fig, ax = plt.subplots()
    data['drawdown'].plot(ax=ax, color="red", lw=2.)
    ax.set_title("Drawdowns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdowns, %")
    st.pyplot(fig)

def main():
    st.title("Backtest Results Dashboard")
    
    # Load data
    data = load_data()

    # Display key metrics
    st.header("Key Metrics")
    total_return = f"{(data['equity_curve'].iloc[-1] - 1.0) * 100:.2f}%"
    max_drawdown = f"{data['drawdown'].min() * 100:.2f}%"
    st.metric("Total Return", total_return)
    st.metric("Max Drawdown", max_drawdown)

    # Display plots
    st.header("Equity Curve")
    plot_equity_curve(data)
    
    st.header("Period Returns")
    plot_returns(data)
    
    st.header("Drawdowns")
    plot_drawdowns(data)

if __name__ == "__main__":
    main()
