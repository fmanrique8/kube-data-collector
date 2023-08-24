"""
This is a boilerplate pipeline 'forex_processor'
generated using Kedro 0.18.12
"""

import pandas as pd
from kube_data_collector.utils.data_processing.utils import (
    convert_to_datetime,
    round_columns,
)


def data_processor_node(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the input DataFrame using a sequence of transformations.

    Args:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """
    # Using pandas pipe to apply sequence of transformations
    df = (
        df.pipe(convert_to_datetime, column_name="date").pipe(
            round_columns, columns=["open", "high", "low", "close"], decimals=5
        )
        # Ensure correct dtypes
        .astype(
            {
                "instrument": "str",
                "open": "float",
                "high": "float",
                "low": "float",
                "close": "float",
            }
        )
    )
    return df
