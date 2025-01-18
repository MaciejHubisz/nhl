import requests


def fetch_html(url: str) -> str:
    """
    Pobiera zawartość HTML z podanego URL.

    Args:
        url (str): URL strony.

    Returns:
        str: Treść HTML strony jako tekst, lub None w przypadku błędu.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Sprawdza, czy odpowiedź jest 200 OK
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return None
