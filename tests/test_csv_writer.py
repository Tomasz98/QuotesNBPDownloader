import unittest
import os
import csv
from file_management.csv_writer import (
    save_all_currency_data_to_csv,
    save_selected_data_to_csv,
)
from datetime import datetime


class TestCurrencyDataCSV(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {
                "date": datetime(2023, 1, 1),
                "eur_pln": 4.5,
                "usd_pln": 3.8,
                "chf_pln": 4.0,
                "eur_usd": 1.2,
                "chf_usd": 1.05,
            },
            {
                "date": datetime(2023, 1, 2),
                "eur_pln": 4.6,
                "usd_pln": 3.9,
                "chf_pln": 4.1,
                "eur_usd": 1.18,
                "chf_usd": 1.06,
            },
        ]

    def test_save_all_currency_data_to_csv(self):
        """
        Test the 'save_all_currency_data_to_csv' function to ensure it correctly creates and writes data to a CSV file.

        """
        save_all_currency_data_to_csv(self.test_data)
        self.assertTrue(os.path.exists("all_currency_data.csv"))

        with open("all_currency_data.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            self.assertEqual(
                headers, ["date", "eur_pln", "usd_pln", "chf_pln", "eur_usd", "chf_usd"]
            )

    def test_save_selected_data_to_csv(self):
        """
        Test the 'save_selected_data_to_csv' function to ensure it correctly creates and writes data to a CSV file.

        """
        selected_pairs = ["eur_pln", "eur_usd"]
        save_selected_data_to_csv(self.test_data, selected_pairs)
        self.assertTrue(os.path.exists("selected_currency_data.csv"))

        with open("selected_currency_data.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            self.assertEqual(headers, ["date"] + selected_pairs)

    def tearDown(self):
        """
        Deleting files after testing.
        This method navigates to the parent directory and deletes 'all_currency_data.csv'
        and 'selected_currency_data.csv' if they exist.
        """
        parent_dir = os.path.dirname(os.getcwd())
        all_currency_file = os.path.join(parent_dir, "all_currency_data.csv")
        selected_currency_file = os.path.join(parent_dir, "selected_currency_data.csv")

        if os.path.exists(all_currency_file):
            os.remove(all_currency_file)

        if os.path.exists(selected_currency_file):
            os.remove(selected_currency_file)


if __name__ == "__main__":
    unittest.main()
