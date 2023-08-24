"""
This is a boilerplate pipeline 'forex_feature'
generated using Kedro 0.18.12
"""

import pandas as pd


def compute_momentum_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes a momentum score for the provided DataFrame based on the ROC, RSI, and Stochastic indicators.

    The momentum score is a weighted sum of the scores assigned to the signals of the ROC, RSI, and Stochastic
    indicators. Each signal can take one of the following values: 'Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell',
    and each of these signals is assigned a numerical score. The weighted sum of these scores gives the momentum score
    for each row in the DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame with columns 'ROC_signal', 'RSI_signal', and 'Stochastic_signal' containing
      the signals for the respective indicators.

    Returns:
    - pd.DataFrame: The input DataFrame augmented with the 'momentum_score_num' column containing the numerical momentum
      score, and the 'momentum_score' column containing the label for the momentum score.
    """
    # Weights for each indicator
    ROC_weight = 0.2
    RSI_weight = 0.5
    Stochastic_weight = 0.4

    # Scoring system
    signal_scores = {
        "Strong Buy": 2,
        "Buy": 1,
        "Hold": 0,
        "Sell": -1,
        "Strong Sell": -2,
    }

    # Compute weighted scores for each indicator
    df["ROC_score"] = df["ROC_signal"].map(signal_scores) * ROC_weight
    df["RSI_score"] = df["RSI_signal"].map(signal_scores) * RSI_weight
    df["Stochastic_score"] = (
        df["Stochastic_signal"].map(signal_scores) * Stochastic_weight
    )

    # Sum up the scores to get the momentum score
    df["momentum_score_num"] = df[["ROC_score", "RSI_score", "Stochastic_score"]].sum(
        axis=1
    )

    # Assign momentum score labels based on momentum score num
    df["momentum_score"] = pd.cut(
        df["momentum_score_num"],
        bins=[-float("inf"), -1.5, -0.5, 0.5, 1.5, float("inf")],
        labels=["Strong Sell", "Sell", "Hold", "Buy", "Strong Buy"],
    )

    # Drop the temporary score columns
    df = df.drop(["ROC_score", "RSI_score", "Stochastic_score"], axis=1)

    return df


def forex_feature_node(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Process the input DataFrame using a sequence of transformations.

    Args:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """
    # Using pandas pipe to apply sequence of transformations
    df = df.pipe(compute_momentum_score)
    return df
