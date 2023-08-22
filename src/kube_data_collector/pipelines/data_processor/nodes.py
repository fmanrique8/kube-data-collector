"""
This is a boilerplate pipeline 'data_processor'
generated using Kedro 0.18.12
"""

import pandas as pd
import pytz


def convert_to_datetime(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Convert a specified column of a DataFrame to datetime type.

    Args:
    - df (pd.DataFrame): The input DataFrame.
    - column_name (str): Name of the column in the DataFrame to convert. Default is 'date'.

    Returns:
    - pd.DataFrame: The updated DataFrame with the specified column converted to datetime type.
    """

    # Check if the provided column_name exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Convert specified column to datetime
    df[column_name] = pd.to_datetime(df[column_name])

    # If the datetime values aren't timezone-aware, localize to UTC
    if df[column_name].dt.tz is None:
        df[column_name] = df[column_name].dt.tz_localize("UTC")

    # Convert the datetime from UTC to New York timezone
    new_york = pytz.timezone("America/New_York")
    df[column_name] = df[column_name].dt.tz_convert(new_york)

    return df


def round_columns(df: pd.DataFrame, columns: list, decimals: int) -> pd.DataFrame:
    """
    Rounds specified columns of a DataFrame to a given number of decimals.

    Args:
    - df (pd.DataFrame): The input DataFrame.
    - columns (list): List of column names to be rounded.
    - decimals (int): Number of decimals to round to.

    Returns:
    - pd.DataFrame: The updated DataFrame with the specified columns rounded.
    """

    # Check if all provided columns exist in the DataFrame
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame.")

    # Round specified columns
    df[columns] = df[columns].round(decimals)

    return df


def data_processor_node(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the input DataFrame using a sequence of transformations.

    Args:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """
    # Using pandas pipe to apply sequence of transformations
    df = df.pipe(convert_to_datetime, column_name="date").pipe(
        round_columns, columns=["open", "high", "low", "close"], decimals=5
    )
    return df
