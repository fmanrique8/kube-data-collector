# src/kube_data_collector/utils/FetchInstruments.py

"""
This module provides the FetchInstruments class to fetch instrument data from a given API.
"""

import requests
from kube_data_collector import logger


class FetchInstruments:
    """
    A class to interact with the OANDA v20 API for fetching instrument data.
    Attributes:
        BASE_URL (str): The base URL for the API endpoint.
        ENDPOINT (str): The specific endpoint for fetching instrument data.
        HEADERS (dict): Default headers to use with API requests.
    """

    BASE_URL = None
    ENDPOINT = None
    HEADERS = {"Accept-Datetime-Format": "RFC3339"}  # Example format, change as needed

    def __init__(self, access_token, accountID, base_url=None, endpoint=None):
        """
        Initialize an instance of the FetchInstruments class.
        Parameters:
            access_token (str): The API access token.
            base_url (str, optional): The base URL for the API. Defaults to None.
            endpoint (str, optional): The specific endpoint for fetching instrument data. Defaults to None.
        """
        logger.info("Initializing FetchInstruments instance.")
        self.HEADERS = {
            "Accept-Datetime-Format": "RFC3339",
            "Authorization": f"Bearer {access_token}",
        }
        self.accountID = accountID
        if base_url:
            self.BASE_URL = base_url
        if endpoint:
            self.ENDPOINT = endpoint

    def fetch_candles(self, instrument, **kwargs):
        """
        Fetches the instrument candlestick data from OANDA v20 API.
        Parameters:
            - instrument (str): The financial instrument to fetch.
            - **kwargs: Additional parameters for the request.
        Returns:
            - dict: Parsed JSON data from the API response.
        """
        url = f"{self.BASE_URL}/accounts/{self.accountID}/instruments/{instrument}/candles"

        logger.info(f"Fetching data from URL: {url}")
        response = requests.get(url, headers=self.HEADERS, params=kwargs)

        if response.status_code == 200:
            logger.info(f"Successfully fetched candles for instrument: {instrument}")
            return response.json()
        else:
            logger.error(
                f"Error {response.status_code} when fetching candles for {instrument}: {response.text}"
            )
            return None

    def fetch_all_candles(self, instruments, **kwargs):
        """
        Fetches the candlestick data for multiple instruments from OANDA v20 API.

        Parameters:
            - instruments (list): List of financial instruments to fetch.
            - **kwargs: Additional parameters for the request.

        Returns:
            - dict: A dictionary containing each instrument as a key and its corresponding parsed JSON data as value.
        """
        datasets = {}
        for instrument in instruments:
            data = self.fetch_candles(instrument, **kwargs)
            if data:
                datasets[instrument] = data
            else:
                logger.warning(f"No data retrieved for instrument: {instrument}")
        return datasets
