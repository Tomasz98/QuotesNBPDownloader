import requests
from datetime import datetime, timedelta


class DataFetcher:
    """
    DataFetcher is a class for fetching exchange rates from the National Bank of Poland's API.

    Attributes:
        base_url (str): The base URL for the API endpoint.
        currencies (list): List of currency codes for which exchange rates are to be fetched.
        format (str): The format in which to receive data from the API (default is JSON).
    """

    def __init__(self):
        self.base_url = "http://api.nbp.pl/api/exchangerates/rates/A"
        self.currencies = ["EUR", "USD", "CHF"]
        self.format = "json"

    def fetch_exchange_rates(self, days):
        """
        Fetches exchange rates for the predefined set of currencies over a specified number of days.
        Args:
            days (int): The number of days in the past for which to fetch exchange rates.
        Returns:
            dict: A dictionary with currency codes as keys and their respective exchange rates data as values.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        rates = {
            currency: self.fetch_currency_rate(currency, start_date, end_date)
            for currency in self.currencies
        }
        return rates

    def fetch_currency_rate(self, currency, start_date, end_date):
        """
        Fetches the exchange rate for a specific currency between two dates.
        Args:
            currency (str): The currency code for which to fetch the exchange rate.
            start_date (datetime): The start date for the exchange rate data.
            end_date (datetime): The end date for the exchange rate data.

        Returns:
            dict: The JSON response from the API containing exchange rate data for the specified currency.
        """
        url = f"{self.base_url}/{currency}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}/?format={self.format}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
