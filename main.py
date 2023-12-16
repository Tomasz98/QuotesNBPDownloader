import argparse
import json
from data_processing.data_processor import calculate_currency_statistics
from data_fetching.data_fetcher import DataFetcher
from database.database_management import save_to_database, read_data_from_database
from file_management import csv_writer
from data_processing.data_processor import process_currency_data


def parse_int(value):
    try:
        if value is None:
            raise "Wartośc flagi --days jest wymagana"
        else:
            return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Niepoprawna liczba dni: '{value}'. Proszę podać wartość liczbową."
        )


def main():
    allowed_currencies = ["eur_pln", "usd_pln", "chf_pln", "eur_usd", "chf_usd"]

    parser = argparse.ArgumentParser(description="Currency Data Management Tool")
    parser.add_argument(
        "--currency",
        help='Wybierz walutę(y) "eur_pln" / "eur_pln usd_pln", jako separator pomiędzy walutami zastosuj spację.'
             ' Aby wybrać wszystkie waluty wybierz "*" ',
        required=False,
    )
    parser.add_argument(
        "--days", help="Liczba dni do analizy", type=parse_int, required=True
    )
    parser.add_argument(
        "--stat",
        help='Wyświetla statystyki dotyczące wybranych par walut. '
             'Aby skorzystać ze statystyk po fladze --stat napisz "True". ',
        required=False,
    )

    args = parser.parse_args()

    if args.currency != "*":
        currencies = args.currency.split(" ")
        for currency in currencies:
            if currency not in allowed_currencies:
                parser.error(
                    f"Błędna para walut: {currency}. Dozwolone pary to: {', '.join(allowed_currencies)}"
                )
    else:
        currencies = allowed_currencies

    fetcher = DataFetcher()
    exchange_rates = fetcher.fetch_exchange_rates(args.days)
    json_formatted_data = json.dumps(exchange_rates, indent=2)
    formatted_data = json.loads(json_formatted_data)
    processed_data = process_currency_data(formatted_data)
    print(processed_data)
    save_to_database(processed_data)

    data = read_data_from_database(currencies, args.days)

    if args.stat == "True":
        csv_writer.save_selected_data_to_csv(data=data, selected_pairs=currencies)
        for currency in currencies:
            calculate_currency_statistics(currency, args.days)
    else:
        csv_writer.save_all_currency_data_to_csv(data)


main()
