from flask import Flask, render_template, jsonify
from shift_report import fetch_shift_report
from roster_report import fetch_player_roster
import pandas as pd

app = Flask(__name__)

# Funkcja do przygotowania finalnego datasetu
def prepare_dataset():
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

    # Scalanie danych dla drużyny wyjazdowej
    merged_data_away = pd.merge(
        shift_data_away,
        roster_data_away[["Number", "Position"]],
        on="Number",
        how="left"
    )
    merged_data_away.insert(merged_data_away.columns.get_loc("Player Name"), "Position", merged_data_away.pop("Position"))

    # Połączenie danych obu drużyn
    final_dataset = pd.concat([merged_data_home, merged_data_away], ignore_index=True)
    return final_dataset

# Endpoint do pobierania danych jako JSON
@app.route("/data")
def data():
    dataset = prepare_dataset()
    return jsonify(dataset.to_dict(orient="list"))

# Strona główna serwująca interfejs użytkownika
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
