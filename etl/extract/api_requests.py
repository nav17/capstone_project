import requests

# API request function


def request_to_api(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Connection successful!")
        route_data = response.json()
        return route_data
    else:
        print("Error:", response.status_code)