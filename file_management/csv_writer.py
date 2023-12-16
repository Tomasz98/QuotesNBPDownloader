import csv


def save_all_currency_data_to_csv(data):
    """
    Saves all exchange rate data to a CSV file - 'all_currency_data.csv'
    Args:
        data (list of dict): List of dictionaries containing exchange rate data.
    """
    all_pairs = ["eur_pln", "usd_pln", "chf_pln", "eur_usd", "chf_usd"]

    headers = ["date"] + all_pairs

    with open("all_currency_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for record in data:
            date_str = record["date"].strftime("%Y-%m-%d")
            row = [date_str] + [str(record.get(pair, "N/A")) for pair in all_pairs]
            writer.writerow(row)

    print(f"Zapisano wszystkie dane walutowe w all_currency_data.csv")


def save_selected_data_to_csv(data, selected_pairs):
    """
    Saves selected exchange rate data to a CSV file = 'selected_currency_data.csv'

    Args:
        data (list of dict): List of dictionaries containing exchange rate data.
        selected_pairs (list of str): List of currency pair keys to include in the CSV.
    """
    headers = ["date"] + selected_pairs

    with open(
        "selected_currency_data.csv", mode="w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for record in data:
            date_str = record["date"].strftime("%Y-%m-%d")
            row = [date_str] + [str(record.get(pair, "N/A")) for pair in selected_pairs]
            writer.writerow(row)

    print(
        f"Zapisano wybrane dane walutowe ({','.join(selected_pairs)}) w selected_currency_data.csv"
    )
