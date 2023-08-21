
# Pipeline forex_collector

> *Note:* This is a `README.md` boilerplate updated based on the `forex_data_collector_node` function.

## Overview

This pipeline contains the `forex_data_collector_node` function, which is designed to fetch and process forex data based on given configurations. The function interacts with an external API to fetch instrument data and subsequently processes this data to create a master dataframe.

## Pipeline inputs

- **config_name (str):** Name of the configuration to be used (e.g., '10_min', '15_min', '30_min').
- **access_token (str):** The API access token.
- **accountID (str):** Account ID for the API.
- **base_url (str):** The base URL for the API.
- **endpoint (str):** The specific endpoint for fetching instrument data.
- **forex_collector_config (dict):** Configurations from the forex_collector.yml file.

## Pipeline outputs

- **master_dataframe (pd.DataFrame):** Processed dataframe with instrument and date as keys, and OHLC (Open, High, Low, Close) values.
