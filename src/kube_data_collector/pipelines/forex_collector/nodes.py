"""
This is a boilerplate pipeline 'forex_collector'
generated using Kedro 0.18.12
"""

import pandas as pd
from kube_data_collector.utils.FetchInstruments import FetchInstruments
from kube_data_collector.utils.CreateDataframe import CreateDataframe


def forex_data_collector_node(
    config_name: str,
    access_token: str,
    accountID: str,
    base_url: str,
    endpoint: str,
    forex_collector_config: dict,
) -> pd.DataFrame:
    """
    A Kedro node function to fetch and process forex data based on given configurations.

    Args:
        config_name: Name of the configuration to be used (e.g., '10_min', '15_min', '30_min').
        access_token: The API access token.
        accountID: Account ID for the API.
        base_url: The base URL for the API.
        endpoint: The specific endpoint for fetching instrument data.
        forex_collector_config: Configurations from the forex_collector.yml file.

    Returns:
        pd.DataFrame: Processed dataframe with instrument and date as keys, and OHLC values.
    """

    # Extract required configurations
    config = forex_collector_config["configurations"].get(config_name)
    instruments = forex_collector_config["instruments"]

    if not config:
        raise ValueError(
            f"Configuration '{config_name}' not found in forex_collector_config."
        )

    # Fetch instrument data
    fetcher = FetchInstruments(access_token, accountID, base_url, endpoint)
    datasets = fetcher.fetch_all_candles(instruments, **config)

    # Process the datasets to create the master dataframe
    dataframe_creator = CreateDataframe(datasets)
    master_dataframe = dataframe_creator.get_master_dataframe()

    return master_dataframe
