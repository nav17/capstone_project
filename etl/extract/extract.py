import requests
import os

# Initial API connection

# An endpoint to test on
url = "https://api.tfl.gov.uk/Line/Route"

# Load API Credentials from .env

app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")

params = {
    'app_id': app_id,
    'app_key': app_key
}

# API request function


def request_to_api(url, params):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Connection successful!")
    else:
        print("Error:", response.status_code)
