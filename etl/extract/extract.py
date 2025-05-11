import pandas as pd
import os
from api_requests import request_to_api

# Initial API connection

# Base URL for the API
base_url = "https://api.tfl.gov.uk/Line/Route"


# Load API Credentials from .env

app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")

params = {
    'app_id': app_id,
    'app_key': app_key
}

# Make the API request
route_data = request_to_api(url=base_url, params=params)
# Save response to DataFrame
df = pd.DataFrame(route_data)
df.to_csv("data/route_data.csv")
print("Data saved to data/route_data.csv")