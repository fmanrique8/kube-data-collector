"""
This is a boilerplate pipeline 'forex_primary'
generated using Kedro 0.18.12
"""

import pandas as pd
from kube_data_collector.utils.technical_indicators.momentum.rate_of_change import (
    calculate_roc,
)
from kube_data_collector.utils.technical_indicators.momentum.relative_strenght_index import (
    calculate_rsi,
)
from kube_data_collector.utils.technical_indicators.momentum.stochastic_oscillator import (
    calculate_stochastic_oscillator,
)
from kube_data_collector.utils.technical_indicators.momentum import (
    compute_momentum_score,
)

from kube_data_collector.utils.data_processing.utils import forward_fill_and_median
from kube_data_collector.utils.data_processing.utils import convert_to_datetime

# from kube_data_collector.utils.data_processing.utils import add_date_features


def forex_primary_node(
    df: pd.DataFrame,
    close_n_periods: int,
    rsi_n_periods: int,
    so_n_periods: int = 14,
) -> pd.DataFrame:
    """
    Process the input DataFrame using a sequence of transformations.

    Args:
    - df (pd.DataFrame): The input DataFrame.
    - close_n_periods (int): The number of periods for the ROC.
    - rsi_n_periods (int): The number of periods for the RSI.
    - so_n_periods (int): The number of periods for the Stochastic Oscillator. Default is 14.
    - so_smoothing (int): The number of periods for the smoothing of %K to get %D. Default is 3.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """

    # Using pandas pipe to apply sequence of transformations
    df = (
        df.pipe(convert_to_datetime, column_name="date")
        .pipe(calculate_roc, column_name="close", close_n_periods=close_n_periods)
        .pipe(calculate_rsi, column_name="close", rsi_n_periods=rsi_n_periods)
        .pipe(
            calculate_stochastic_oscillator,
            close_col="close",
            high_col="high",
            low_col="low",
            n=so_n_periods["n"],
            smoothing=so_n_periods["smoothing"],
        )
        .pipe(compute_momentum_score)
        .pipe(
            forward_fill_and_median,
            columns=[
                "ROC",
                "ROC_signal",
                "ROC_signal_num",
                "RSI",
                "RSI_signal",
                "RSI_signal_num",
                "%K",
                "%D",
                "Stochastic_signal",
                "Stochastic_signal_num",
            ],
        )
        # Ensure correct dtypes and limit float numbers
        .round(
            {"ROC": 5, "ROC_signal": 5, "RSI": 5, "%K": 5, "%D": 5, "momentum_score": 5}
        )
        .astype(
            {
                "ROC_signal_num": "int",
                "RSI_signal_num": "int",
                "Stochastic_signal_num": "int",
            }
        )
    )
    return df
