"""kube-data-collector
"""

from . import signal_num_map, signals
import numpy as np
import pandas as pd


def calculate_rsi(
    df: pd.DataFrame, column_name: str, rsi_n_periods: int = 14
) -> pd.DataFrame:
    """
    Calculate the Relative Strength Index (RSI) for a given DataFrame and column and append it as new columns.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing price data.
    - column_name (str): The column for which to calculate the RSI.
    - rsi_n_periods (int): The number of periods for the RSI calculation (default is 14).

    Returns:
    - pd.DataFrame: The original DataFrame with additional columns for RSI, RSI_signal, and RSI_signal_num.
    """
    # Check if the given column name exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column {column_name} not found in the DataFrame.")

    # Check if rsi_n_periods is a positive integer
    if not isinstance(rsi_n_periods, int) or rsi_n_periods <= 0:
        raise ValueError("rsi_n_periods should be a positive integer.")

    # Calculate daily price changes
    df["delta"] = df[column_name].diff()

    # Separate gains and losses
    df["gain"] = df["delta"].where(df["delta"] > 0, 0)
    df["loss"] = -df["delta"].where(df["delta"] < 0, 0)

    # Calculate average gain and average loss
    avg_gain = df["gain"].rolling(window=rsi_n_periods, min_periods=1).mean()
    avg_loss = df["loss"].rolling(window=rsi_n_periods, min_periods=1).mean()

    # Calculate Relative Strength (RS)
    rs = avg_gain / avg_loss

    # Calculate RSI
    df["RSI"] = 100 - (100 / (1 + rs))

    # Define RSI signals
    conditions = [
        df["RSI"] < 30,
        (df["RSI"] >= 30) & (df["RSI"] < 45),
        (df["RSI"] >= 45) & (df["RSI"] <= 55),
        (df["RSI"] > 55) & (df["RSI"] <= 70),
        df["RSI"] > 70,
    ]
    df["RSI_signal"] = np.select(conditions, signals, default="N/A")
    df["RSI_signal_num"] = df["RSI_signal"].map(signal_num_map)

    # Drop intermediate columns used for calculations
    df.drop(columns=["delta", "gain", "loss"], inplace=True)

    return df
