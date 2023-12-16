import unittest
from unittest.mock import patch, MagicMock
from database.database_management import read_data_from_database


class TestDatabaseOperations(unittest.TestCase):
    @patch("database.database_management.Session")
    def test_read_data_from_database(self, mock_session_class):

        mock_session = mock_session_class.return_value
        mock_session.execute.return_value.fetchall.return_value = [
            (
                MagicMock(
                    date="2021-04-30",
                    eur_pln=4.5581,
                    usd_pln=3.7821,
                    chf_pln=4.1287,
                    eur_usd=1.2045,
                    chf_usd=1.0917,
                ),
            )
        ]

        result = read_data_from_database(["eur_pln", "usd_pln"], 10)

        self.assertEqual(len(result), 1)
        self.assertIn("eur_pln", result[0])
        self.assertIn("usd_pln", result[0])
        self.assertNotIn("chf_pln", result[0])


if __name__ == "__main__":
    unittest.main()
