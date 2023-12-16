import unittest
from unittest.mock import patch, MagicMock
from database.single_session import SingletonSession


class TestSingletonSession(unittest.TestCase):
    def setUp(self):
        SingletonSession._session_factory = None

    @patch("database.single_session.create_engine")
    @patch("database.single_session.sessionmaker")
    def test_initialize_session_creates_session_factory(
        self, mock_sessionmaker, mock_create_engine
    ):
        """
        Test whether the initialize_session method correctly initializes the session factory.
        """
        mock_engine = mock_create_engine.return_value
        mock_sessionmaker.return_value = MagicMock()

        SingletonSession.initialize_session()

        mock_create_engine.assert_called_once()
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)

    @patch("database.single_session.create_engine")
    def test_get_session_returns_session(self):
        """
        Test whether the get_session method returns a session instance.
        """

        SingletonSession._session_factory = None

        with patch("database.single_session.scoped_session") as mock_scoped_session:
            session = SingletonSession.get_session()
            self.assertIsNotNone(session)
            mock_scoped_session.assert_called_once()

    @patch("database.single_session.create_engine")
    def test_session_factory_is_singleton(self):
        """
        Test whether the session factory is created only once..
        """
        SingletonSession._session_factory = None

        with patch("database.single_session.scoped_session") as mock_scoped_session:
            session1 = SingletonSession.get_session()
            session2 = SingletonSession.get_session()
            self.assertEqual(session1, session2)
            mock_scoped_session.assert_called_once()


if __name__ == "__main__":
    unittest.main()
