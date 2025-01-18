from utils import fetch_html

url = "https://www.nhl.com/scores/htmlreports/20242025/TV020637.HTM"
html_content = fetch_html(url)

if html_content:
    print("HTML content fetched successfully!")
else:
    print("Failed to fetch HTML content.")
