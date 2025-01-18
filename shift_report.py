import pandas as pd
from bs4 import BeautifulSoup
from utils import fetch_html

BASE_URL = "https://www.nhl.com/scores/htmlreports"

def fetch_shift_report(home_team: str, away_team: str, game_date: str, manual_url: str = None) -> pd.DataFrame:
    """
    Fetch shift report data for a given NHL game.

    Args:
        home_team (str): Abbreviation of the home team (e.g., "NYR" for New York Rangers).
        away_team (str): Abbreviation of the away team (e.g., "BOS" for Boston Bruins).
        game_date (str): Date of the game in "YYYY-MM-DD" format.
        manual_url (str, optional): If provided, overrides the generated URL.

    Returns:
        pd.DataFrame: DataFrame containing shift report data with separate Player Number and Name columns.
    """
    # Generate the season and game ID
    season_start_year = int(game_date[:4])
    season = f"{season_start_year}{season_start_year + 1}"
    game_id = f"02{home_team}{away_team}"

    # Generate or use the manual URL
    shift_url = manual_url
    print(f"Fetching shift report from URL: {shift_url}")

    # Fetch the HTML content
    html_content = fetch_html(shift_url)
    if not html_content:
        raise ValueError(f"Failed to fetch HTML content from the URL: {shift_url}")

    # Parse the HTML
    soup = BeautifulSoup(html_content, "lxml")

    # Initialize variables
    all_data = []
    current_player = None

    # Find all rows in the HTML
    rows = soup.find_all("tr")

    for row in rows:
        # Check for player heading
        player_heading = row.find("td", class_="playerHeading")
        if player_heading:
            current_player = player_heading.text.strip()
            continue  # Skip to the next row

        # Ignore spacer rows
        if row.find("td", class_="spacer"):
            continue

        # Extract table data
        cells = row.find_all("td")
        if cells:
            data_row = [cell.text.strip() for cell in cells]
            # Skip rows that are actually headers (e.g., containing "Shift #")
            if "Shift #" in data_row or "Duration" in data_row:
                continue
            # Add the current player to the row
            all_data.append([current_player] + data_row)

    # Define the columns
    columns = ["Player", "Shift #", "Per", "Start of Shift", "End of Shift", "Duration", "Event"]

    # Filter the data to match the columns
    filtered_data = [row for row in all_data if len(row) == len(columns)]

    # Create DataFrame
    df = pd.DataFrame(filtered_data, columns=columns)

    # Remove the "Event" column
    if "Event" in df.columns:
        df = df.drop(columns=["Event"])

    # Split "Player" into "Number" and "Player Name"
    df[['Number', 'Player Name']] = df['Player'].str.extract(r'(\d+)\s+(.+)')
    df = df.drop(columns=["Player"])

    # Reorder columns for readability
    df = df[["Number", "Player Name", "Shift #", "Per", "Start of Shift", "End of Shift", "Duration"]]

    return df
