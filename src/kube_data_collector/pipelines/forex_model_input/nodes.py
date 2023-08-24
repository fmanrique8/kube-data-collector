"""
This is a boilerplate pipeline 'forex_model_input'
generated using Kedro 0.18.12
"""

import pandas as pd
from kube_data_collector.utils.data_processing.utils import (
    convert_to_datetime,
)


def rank_instruments_by_momentum_avg(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    Rank instruments based on the average of momentum_score_num and return both top 3 and bottom 3 instruments.

    Args:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - top_3_df (pd.DataFrame): The top 3 instruments based on average momentum_score_num.
    - bottom_3_df (pd.DataFrame): The bottom 3 instruments based on average momentum_score_num.
    """
    # Group by instrument and compute the average of momentum_score_num
    avg_momentum = df.groupby("instrument")["momentum_score_num"].mean().reset_index()

    # Sort the DataFrame based on average momentum_score_num
    sorted_avg_momentum = avg_momentum.sort_values(
        by="momentum_score_num", ascending=False
    )

    # Retrieve the top 3 and bottom 3 instruments
    top_3_df = sorted_avg_momentum.head(3)
    bottom_3_df = sorted_avg_momentum.tail(3)

    return top_3_df, bottom_3_df


def forex_model_input_node(
    df: pd.DataFrame,
) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Process the input DataFrame using a sequence of transformations.

    Args:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - original_df (pd.DataFrame): The original processed DataFrame.
    - top_3_df (pd.DataFrame): The top 3 instruments based on average momentum_score_num.
    - bottom_3_df (pd.DataFrame): The bottom 3 instruments based on average momentum_score_num.
    """
    # Convert date column to datetime
    df = df.pipe(convert_to_datetime, column_name="date")

    # List of desired columns
    columns = [
        "instrument",
        "date",
        "close",
        "ROC_signal_num",
        "RSI_signal_num",
        "Stochastic_signal_num",
        "momentum_score_num",
        "ROC_signal",
        "Stochastic_signal",
        "momentum_score",
        "RSI_signal",
    ]

    # Filter dataframe to only include desired columns
    df = df.loc[:, columns]

    # Get the top 3 and bottom 3 instruments based on average momentum_score_num
    top_3_df, bottom_3_df = rank_instruments_by_momentum_avg(df)

    return df, top_3_df, bottom_3_df
