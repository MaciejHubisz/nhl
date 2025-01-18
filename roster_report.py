import pandas as pd
from bs4 import BeautifulSoup
from utils import fetch_html

BASE_URL = "https://www.nhl.com/scores/htmlreports"

def fetch_player_roster(home_team: str, away_team: str, game_date: str, manual_url: str = None, team: str = "home") -> pd.DataFrame:
    season_start_year = int(game_date[:4])
    season = f"{season_start_year}{season_start_year + 1}"
    game_id = f"02{home_team}{away_team}"

    roster_url = manual_url
    print(f"Fetching player roster from URL: {roster_url}")

    html_content = fetch_html(roster_url)
    if not html_content:
        raise ValueError(f"Failed to fetch HTML content from the URL: {roster_url}")

    soup = BeautifulSoup(html_content, "lxml")

    # Find all team tables
    team_tables = [table for table in soup.find_all("table") if table.find("td", class_="heading + bborder")]
    print(f"Found {len(team_tables)} team tables.")

    # Determine which team's table to parse
    team_index = 0 if team == "home" else 1
    if len(team_tables) <= team_index:
        raise ValueError(f"No table found for team index {team_index}. Check HTML structure.")

    team_table = team_tables[team_index]

    # Extract player data
    players = []
    rows = team_table.find_all("tr")[1:]  # Skip the header row
    print(f"Found {len(rows)} rows in the team table.")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 3:
            # Extract values and skip invalid rows
            number = cells[0].text.strip()
            position = cells[1].text.strip()
            name = cells[2].text.strip()

            # Ignore rows that are empty or contain invalid headers
            if not number.isdigit():  # Ensure 'number' is a valid player number
                continue
            players.append([number, position, name])

    # Create DataFrame
    columns = ["Number", "Position", "Name"]
    return pd.DataFrame(players, columns=columns)
