import unittest
from unittest.mock import patch, Mock
import requests
from data_fetching.data_fetcher import DataFetcher
from datetime import datetime


class TestDataFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = DataFetcher()

    @patch("requests.get")
    def test_fetch_currency_rate_network_error(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.fetcher.fetch_currency_rate(
                "EUR", datetime(2023, 1, 1), datetime(2023, 1, 2)
            )

    @patch("requests.get")
    def test_fetch_currency_rate_http_error(self, mock_get):

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.fetcher.fetch_currency_rate(
                "EUR", datetime(2023, 1, 1), datetime(2023, 1, 2)
            )


if __name__ == "__main__":
    unittest.main()
