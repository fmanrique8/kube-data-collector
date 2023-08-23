"""
This is a boilerplate pipeline 'forex_model_input'
generated using Kedro 0.18.12
"""

import pandas as pd
from kube_data_collector.utils.data_processing.utils import (
    convert_to_datetime,
)


def forex_model_input_node(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the input DataFrame using a sequence of transformations.

    Args:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """
    df = (
        df.pipe(convert_to_datetime, column_name="date")

    )
    return df
