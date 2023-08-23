# src/kube_data_collector/utils/CreateDataframe.py

"""
This module provides the CreateDataframe class, which processes datasets from the FetchInstruments class and
converts them into a unified dataframe format, with 'instrument' and 'date' serving as the primary keys.
"""

import pandas as pd
from kube_data_collector import logger


class CreateDataframe:
    """
    A class to convert datasets fetched from the FetchInstruments class into a master dataframe.

    Attributes:
        datasets (dict): The datasets obtained from the FetchInstruments class.
    """

    def __init__(self, datasets):
        """
        Initialize an instance of the CreateDataframe class.

        Parameters:
            datasets (dict): Datasets obtained from the FetchInstruments class.
        """
        self.datasets = datasets
        logger.info("Initializing CreateDataframe instance.")

    def process_data(self):
        """
        Processes the datasets to create a master dataframe.

        This function converts the datasets from the FetchInstruments class into a unified dataframe format.
        Each entry in the dataframe corresponds to a candlestick entry for a particular financial instrument on a particular date.

        Returns:
            pd.DataFrame: A master dataframe with 'instrument' and 'date' as keys, and containing OHLC values.
        """
        logger.info("Processing data to create the master dataframe.")
        master_data = []

        for instrument, data in self.datasets.items():
            for entry in data.get(
                "candles", []
            ):  # Assuming 'candles' is the key that contains the list of data entries
                master_data.append(
                    {
                        "instrument": instrument,
                        "date": entry.get(
                            "time"
                        ),  # Assuming 'time' is the key that contains the date
                        "open": entry.get("mid", {}).get("o"),
                        "high": entry.get("mid", {}).get("h"),
                        "low": entry.get("mid", {}).get("l"),
                        "close": entry.get("mid", {}).get("c"),
                    }
                )

        logger.info("Data processing completed. Master dataframe created.")
        return pd.DataFrame(master_data)

    def get_master_dataframe(self):
        """
        Retrieves the master dataframe.

        This function calls the process_data function and retrieves the resulting dataframe.

        Returns:
            pd.DataFrame: The master dataframe.
        """
        logger.info("Fetching the master dataframe.")
        return self.process_data()
