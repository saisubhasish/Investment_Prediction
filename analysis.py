import sys
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from investment_prediction.config import collection_name
from investment_prediction.exception import InvestmentPredictionException



def plot_sma(df, window_size= 200):
    """
    Description: This function plots Simple Moving Average
    =========================================================
    Params:
    df: dataframe
    window_size: Number of days you wants to consider (eg. 50, 100 etc)
                    Default is 200
    =========================================================
    """
    try:
        plt.figure(figsize=(15,5))
        df['SMA'] = df['Price'].rolling(window=window_size).mean()
        plt.plot(df['Price'], label='Price')
        plt.plot(df['SMA'], label=f'{window_size}-day SMA')
        plt.title(f"{window_size}-Day Simple Moving Average Chart for {collection_name}")
        plt.xlabel("Year")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    except Exception as e:
        raise InvestmentPredictionException(e, sys)


def plot_ema(df, window_size= 200):
    """
    Description: This function plots Exponential Moving Average
    =========================================================
    Params:
    df: dataframe
    window_size: Number of days you wants to consider (eg. 50, 100 etc)
                    Default is 200
    =========================================================
    """
    try:
        ema = 'EMA'+f'{window_size}'
        df[ema] = df['Price'].ewm(span=window_size, adjust=False).mean()
        df[['Price', ema]].plot(figsize=(10,8))
        plt.title(f"{window_size}-Day Exponential Moving Average Chart for {collection_name}")
        plt.xlabel("Year")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    except Exception as e:
        raise InvestmentPredictionException(e, sys)


def plot_bollinger_band(df):
    """
    Description: This function plots Bollinger Band graph
    =========================================================
    Params:
    df: dataframe
    =========================================================
    """
    try:
        plt.figure(figsize=(15,5))
        df['MA'] = df['Price'].rolling(window=20).mean()
        df['STD'] = df['Price'].rolling(window=20).std()
        df['Upper Band'] = df['MA'] + 2*df['STD']
        df['Lower Band'] = df['MA'] - 2*df['STD']
        plt.plot(df['Price'], label='Price')
        plt.plot(df['Upper Band'], label='Upper Band', linestyle='--')
        plt.plot(df['Lower Band'], label='Lower Band', linestyle='--')
        plt.title(f"Bollinger Bands Chart for {collection_name}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    except Exception as e:
        raise InvestmentPredictionException(e, sys)


def plot_macd(df):
    """
    Description: This function plots MACD Chart
    =========================================================
    Params:
    df: dataframe
    =========================================================
    """
    try:
        # Create the MACD line
        fast_period = 12
        slow_period = 26
        signal_period = 9
        df["MACD"] = df['Price'].ewm(span=fast_period, adjust=False).mean() - df['Price'].ewm(span=slow_period, adjust=False).mean()
        df["Signal"] = df["MACD"].ewm(span=signal_period, adjust=False).mean()

        # Plot the MACD chart
        plt.figure(figsize=(16, 8))
        plt.plot(df['Price'], label='Price')
        plt.plot(df["MACD"], label='MACD')
        plt.plot(df["Signal"], label='Signal')
        plt.legend(loc='best')
        plt.title(f"MACD Chart for {collection_name}")
        plt.show()

    except Exception as e:
        raise InvestmentPredictionException(e, sys)
    
def plot_volume(df):
    """
    Description: This function plots Volume Chart
    =========================================================
    Params:
    df: dataframe
    =========================================================
    """
    top_plt = plt.subplot2grid((5,4), (0, 0), rowspan=3, colspan=4)
    top_plt.plot(df.index, df["Price"])
    plt.title(f'Historical stock prices of {collection_name} [01-04-2016 to 30-09-2020]')
    bottom_plt = plt.subplot2grid((5,4), (3,0), rowspan=1, colspan=4)
    bottom_plt.bar(df.index, df['Volume'])
    plt.title('\nReliance Inds. Trading Volume', y=-0.60)
    plt.gcf().set_size_inches(12,8)

def plot_candle_stick(df):
    """
    Description: This function plots Candle Sick Chart
    =========================================================
    Params:
    df: dataframe
    consisting columns==> Open, High, Low, Close
    =========================================================
    """
    fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Price'])])
    fig.show()
