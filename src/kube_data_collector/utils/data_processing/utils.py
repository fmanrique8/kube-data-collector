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


def add_date_features(df: pd.DataFrame, column_name: str = "date") -> pd.DataFrame:
    """
    Add date-based features to the DataFrame.

    Args:
    - df (pd.DataFrame): The input DataFrame.
    - column_name (str): Name of the date column in the DataFrame. Default is 'date'.

    Returns:
    - pd.DataFrame: The updated DataFrame with new date-based features.
    """

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Extracting various date features
    df["MoH_num"] = df[column_name].dt.minute
    df["HoD_num"] = df[column_name].dt.hour
    df["DoW_num"] = df[column_name].dt.dayofweek
    df["MoY_num"] = df[column_name].dt.month
    df["DoW_cat"] = df[column_name].dt.day_name()
    df["MoY_cat"] = df[column_name].dt.month_name()

    # Calculating week of the month
    df["WoM_num"] = (df[column_name].dt.day - 1) // 7 + 1
    week_map = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth"}
    df["WoM_cat"] = df["WoM_num"].map(week_map)

    return df


def forward_fill_and_median(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Process a DataFrame to handle NaN and "N/A" values.

    1. Replace "N/A" strings with "Hold".
    2. Forward fill NaN values in specified columns.
    3. If any NaNs remain after forward filling:
       - For numeric columns, fill with median.
       - For non-numeric columns, fill with the most frequent value (mode).

    Args:
    - df (pd.DataFrame): Input DataFrame.
    - columns (list): List of column names to process.

    Returns:
    - pd.DataFrame: Processed DataFrame.
    """
    # Replace "N/A" with "Hold"
    df.replace("N/A", "Hold", inplace=True)

    for col in columns:
        # Forward fill
        df[col] = df[col].ffill()

        # If column is numeric, fill remaining NaNs with median
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col].fillna(df[col].median(), inplace=True)
        else:
            # For non-numeric columns, fill with the most frequent value (mode)
            df[col].fillna(df[col].mode().iloc[0], inplace=True)

    return df
