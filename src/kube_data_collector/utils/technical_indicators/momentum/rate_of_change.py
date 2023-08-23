"""kube-data-collector
"""

from . import signal_num_map, signals
import numpy as np
import pandas as pd


def calculate_roc(
    df: pd.DataFrame, column_name: str, close_n_periods: int
) -> pd.DataFrame:
    """
    Calculate the Rate of Change (ROC) for a given DataFrame and column and append it as new columns.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing price data.
    - column_name (str): The column for which to calculate the ROC.
    - close_n_periods (int): The number of periods back for the ROC calculation.

    Returns:
    - pd.DataFrame: The original DataFrame with additional columns for ROC, ROC_signal, and ROC_signal_num.
    """

    # Check if the given column name exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column {column_name} not found in the DataFrame.")

    # Check if close_n_periods is a positive integer
    if not isinstance(close_n_periods, int) or close_n_periods <= 0:
        raise ValueError("close_n_periods should be a positive integer.")

    # Calculate ROC
    df["ROC"] = (
        (df[column_name] - df[column_name].shift(close_n_periods))
        / df[column_name].shift(close_n_periods)
    ) * 100

    # Define ROC signals
    conditions = [
        df["ROC"] > 10,
        (df["ROC"] > 5) & (df["ROC"] <= 10),
        (df["ROC"] >= -5) & (df["ROC"] <= 5),
        (df["ROC"] < -5) & (df["ROC"] >= -10),
        df["ROC"] <= -10,
    ]
    df["ROC_signal"] = np.select(conditions, signals, default="N/A")
    df["ROC_signal_num"] = df["ROC_signal"].map(signal_num_map)

    return df
