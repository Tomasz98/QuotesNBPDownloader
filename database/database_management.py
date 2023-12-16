from sqlalchemy import select, desc
from datetime import datetime, timedelta
from database.models import ExchangeRate
from database.single_session import SingletonSession


def save_to_database(data):
    """
    Saves exchange rate data to the database.

    Args:
        data: A list of dictionaries, each containing the exchange rate information for a particular date.
              Each dictionary must have the following keys: 'date', 'eur_pln', 'usd_pln', 'chf_pln', 'eur_usd', 'chf_usd'.
    """
    session = SingletonSession.get_session()
    with session:
        for item in data:
            date_obj = datetime.strptime(item["date"], "%Y-%m-%d").date()
            existing_rate = session.query(ExchangeRate).filter_by(date=date_obj).first()

            if existing_rate:
                continue

            rate = ExchangeRate(
                date=date_obj,
                eur_pln=item["eur_pln"],
                usd_pln=item["usd_pln"],
                chf_pln=item["chf_pln"],
                eur_usd=item["eur_usd"],
                chf_usd=item["chf_usd"],
            )
            session.add(rate)

        session.commit()
        session.close()





def read_data_from_database(currencies, days):
    """
    Czyta i filtruje dane o kursach walutowych z bazy danych.

    Args:
        currencies (list): Lista ciągów znaków wskazujących, które kursy walut należy uwzględnić w wyniku.
        days (int): Liczba dni wstecz od aktualnej daty, dla której należy pobrać dane.

    Returns:
        list of dict: Lista słowników, każdy zawierający przefiltrowane dane o kursie walutowym dla danej daty.
    """
    session = SingletonSession.get_session()
    with session:
        start_date = datetime.now() - timedelta(days=days)
        query = (
            select(ExchangeRate)
            .where(ExchangeRate.date >= start_date)
            .order_by(desc(ExchangeRate.date))
        )
        result = session.execute(query).scalars().all()

        filtered_data = []
        for record in result:
            data = {currency: getattr(record, currency) for currency in currencies if hasattr(record, currency)}
            data["date"] = record.date  # Zawsze dołączaj datę do każdego słownika
            filtered_data.append(data)

        return filtered_data  # Nie ma potrzeby wywoływania session.close() przy użyciu menedżera kontekstu

