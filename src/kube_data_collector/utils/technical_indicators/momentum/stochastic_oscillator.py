"""kube-data-collector
"""

from . import signal_num_map
import numpy as np
import pandas as pd


def calculate_stochastic_oscillator(
    df: pd.DataFrame,
    close_col: str,
    high_col: str,
    low_col: str,
    n: int = 14,
    smoothing: int = 3,
) -> pd.DataFrame:
    """
    Calculate the Stochastic Oscillator for a given DataFrame and generate trading signals.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing price data.
    - close_col (str): The column name of closing prices.
    - high_col (str): The column name of high prices.
    - low_col (str): The column name of low prices.
    - n (int): The number of periods for the Stochastic Oscillator.
    - smoothing (int): The number of periods for the smoothing of %K to get %D.

    Returns:
    - pd.DataFrame: The original DataFrame with additional columns for %K, %D, and Stochastic_signal.
    """
    # Check if DataFrame has at least n rows
    if df.shape[0] < n:
        raise ValueError(f"DataFrame has less than {n} rows. Cannot compute rolling window of size {n}.")

    # Rest of the function remains the same
    df["Lowest_Low"] = df[low_col].rolling(window=n).min()
    df["Highest_High"] = df[high_col].rolling(window=n).max()
    df["%K"] = 100 * (df[close_col] - df["Lowest_Low"]) / (df["Highest_High"] - df["Lowest_Low"])
    df["%D"] = df["%K"].rolling(window=smoothing).mean()

    # Generate signals based on the crossing of %K and %D
    conditions = [
        (df["%K"] < 20),
        (df["%K"] > df["%D"]) & (df["%K"].shift(1) <= df["%D"].shift(1)),
        (df["%K"] > 80),
        (df["%K"] < df["%D"]) & (df["%K"].shift(1) >= df["%D"].shift(1)),
    ]
    choices = ["Strong Buy", "Buy", "Strong Sell", "Sell"]
    df["Stochastic_signal"] = np.select(conditions, choices, default="Hold")
    df['Stochastic_signal_num'] = df['Stochastic_signal'].map(signal_num_map)

    # Drop temporary columns
    df.drop(columns=['Lowest_Low', 'Highest_High'], inplace=True)
    return df
