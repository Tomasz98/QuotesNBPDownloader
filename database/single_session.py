from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SingletonSession:
    _session_factory = None

    @staticmethod
    def initialize_session():
        if SingletonSession._session_factory is None:
            DATABASE_URL =  "postgresql://user:password@db/mydatabase"

            engine = create_engine(DATABASE_URL)
            SingletonSession._session_factory = scoped_session(
                sessionmaker(bind=engine)
            )

    @staticmethod
    def get_session():
        if SingletonSession._session_factory is None:
            SingletonSession.initialize_session()
        return SingletonSession._session_factory()
