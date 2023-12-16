from datetime import datetime, timedelta
import numpy as np
from database.models import ExchangeRate
from database.single_session import SingletonSession


def process_currency_data(data):
    """
    Processes exchange rate data for multiple currencies and calculates cross rates.

    This function takes raw exchange rate data for EUR, USD, and CHF against PLN (Polish Zloty) and calculates
    the EUR/USD and CHF/USD cross rates. It assumes the data is structured with 'rates' as a key containing
    a list of rate dictionaries, each with 'effectiveDate' and 'mid' (the exchange rate) as keys.

    Args:
        data (dict): A dictionary containing exchange rate data for multiple currencies.
                     Each currency is a key in this dictionary.

    Returns:
        list: A list of dictionaries, each containing the date, the direct rates against PLN,
              and the calculated cross rates (EUR/USD and CHF/USD).
    """

    eur_rates = data["EUR"]["rates"]
    usd_rates = data["USD"]["rates"]
    chf_rates = data["CHF"]["rates"]

    results = []
    for eur, usd, chf in zip(eur_rates, usd_rates, chf_rates):
        if eur["effectiveDate"] == usd["effectiveDate"] == chf["effectiveDate"]:
            date = eur["effectiveDate"]
            eur_pln = eur["mid"]
            usd_pln = usd["mid"]
            chf_pln = chf["mid"]

            eur_usd = np.round(eur_pln / usd_pln, 4)
            chf_usd = np.round(chf_pln / usd_pln, 4)

            results.append(
                {
                    "date": date,
                    "eur_pln": eur_pln,
                    "usd_pln": usd_pln,
                    "chf_pln": chf_pln,
                    "eur_usd": eur_usd,
                    "chf_usd": chf_usd,
                }
            )

    return results


def calculate_currency_statistics(currency, days):
    """
    Calculates statistical data (average, median, minimum, and maximum) for a given currency's exchange rate over a specified period.

    This function queries a database using SQLAlchemy for exchange rates of a specified currency over the past 'days'.
    It then calculates and prints the average, median, minimum, and maximum values of these rates. The function handles
    the scenario where no data is available for the given period.

    Args:
        currency (str): The currency code for which to calculate statistics (e.g., 'EUR_PLN', 'USD_PLN').
        days (int): The number of days in the past from the current date for which to calculate statistics.

    Note:
        The function prints the calculated statistics to the console and does not return any value.
    """
    session = SingletonSession().get_session()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    query = session.query(getattr(ExchangeRate, currency)).filter(
        ExchangeRate.date.between(start_date, end_date)
    )
    rates = [rate[0] for rate in query.all() if rate[0] is not None]

    if rates:
        avg_rate = np.mean(rates)
        median_rate = np.median(rates)
        min_rate = np.min(rates)
        max_rate = np.max(rates)

        print(f"Statystyki dla {currency}:")
        print(
            f"Średnia: {avg_rate:.5f}, Mediana: {median_rate:.5f}, Minimum: {min_rate:.5f}, Maksimum: {max_rate:.5f}"
        )
    else:
        print(f"Brak danych dla {currency} w ostatnich {days} dniach.")

    session.close()
