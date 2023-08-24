"""kube-data-collector
"""

import pandas as pd

# Map signals to numerical values
signals = ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
signal_num_map = {
    "Strong Buy": 2,
    "Buy": 1,
    "Hold": 0,
    "Sell": -1,
    "Strong Sell": -2,
}


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
    - pd.DataFrame: A DataFrame with columns 'momentum', 'momentum_score_num', and 'momentum_score'.
    """
    # Weights for each indicator
    ROC_weight = 0.1
    RSI_weight = 0.3
    Stochastic_weight = 0.6

    # Compute weighted scores for each indicator
    df["ROC_score"] = df["ROC_signal"].map(signal_num_map) * ROC_weight
    df["RSI_score"] = df["RSI_signal"].map(signal_num_map) * RSI_weight
    df["Stochastic_score"] = (
        df["Stochastic_signal"].map(signal_num_map) * Stochastic_weight
    )

    # Sum up the scores to get the momentum score
    df["momentum"] = df[["ROC_score", "RSI_score", "Stochastic_score"]].sum(axis=1)

    # Round the 'momentum' column to 5 decimal places
    df["momentum"] = df["momentum"].round(5)

    # Assign momentum score labels based on momentum
    df["momentum_score"] = pd.cut(
        df["momentum"],
        bins=[-float("inf"), -1.5, -0.5, 0.5, 1.5, float("inf")],
        labels=["Strong Sell", "Sell", "Hold", "Buy", "Strong Buy"],
    )

    # Map momentum score to its numerical value
    df["momentum_score_num"] = df["momentum_score"].map(signal_num_map)

    # Drop the temporary score columns
    df = df.drop(["ROC_score", "RSI_score", "Stochastic_score"], axis=1)

    return df
