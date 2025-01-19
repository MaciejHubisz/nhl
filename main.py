from flask import Flask, render_template, jsonify
from shift_report import fetch_shift_report
from roster_report import fetch_player_roster
import pandas as pd
import os
import json

app = Flask(__name__)

DATA_FILE = "data.json"

# Funkcja do przygotowania datasetu i zapisania do pliku
def prepare_and_save_dataset():
    home = "WSH"
    away = "BUF"
    date = "2025-01-06"
    manual_shift_url_home = "https://www.nhl.com/scores/htmlreports/20242025/TH020720.HTM"
    manual_shift_url_away = "https://www.nhl.com/scores/htmlreports/20242025/TV020637.HTM"
    manual_roster_url = "https://www.nhl.com/scores/htmlreports/20242025/RO020637.HTM"

    # Pobranie danych shift report dla obu drużyn
    shift_data_home = fetch_shift_report(home, away, date, manual_url=manual_shift_url_home)
    shift_data_away = fetch_shift_report(home, away, date, manual_url=manual_shift_url_away)

    # Pobranie danych roster dla obu drużyn
    roster_data_home = fetch_player_roster(home, away, date, manual_url=manual_roster_url, team="home")
    roster_data_away = fetch_player_roster(home, away, date, manual_url=manual_roster_url, team="away")

    # Scalanie danych dla drużyny domowej
    merged_data_home = pd.merge(
        shift_data_home,
        roster_data_home[["Number", "Position"]],
        on="Number",
        how="left"
    )
    merged_data_home.insert(merged_data_home.columns.get_loc("Player Name"), "Position", merged_data_home.pop("Position"))
    merged_data_home["Team"] = "Home"  # Dodanie kolumny z drużyną

    # Scalanie danych dla drużyny wyjazdowej
    merged_data_away = pd.merge(
        shift_data_away,
        roster_data_away[["Number", "Position"]],
        on="Number",
        how="left"
    )
    merged_data_away.insert(merged_data_away.columns.get_loc("Player Name"), "Position", merged_data_away.pop("Position"))
    merged_data_away["Team"] = "Away"  # Dodanie kolumny z drużyną

    # Połączenie danych obu drużyn
    final_dataset = pd.concat([merged_data_home, merged_data_away], ignore_index=True)

    # Zapis do pliku
    with open(DATA_FILE, "w") as f:
        json.dump(final_dataset.to_dict(orient="list"), f)
    print(f"Dane zapisane do pliku {DATA_FILE}")

# Funkcja do odczytu danych z pliku
def load_dataset():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return data

# Endpoint do pobierania danych jako JSON
@app.route("/data")
def data():
    dataset = load_dataset()
    if dataset is None:
        return jsonify({"error": "Dane nie zostały jeszcze pobrane."}), 404
    return jsonify(dataset)

# Strona główna serwująca interfejs użytkownika
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Pobieranie danych przy starcie serwera
    prepare_and_save_dataset()
    app.run(debug=True)
