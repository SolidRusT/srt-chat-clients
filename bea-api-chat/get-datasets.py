import os
import requests

def get_datasets(api_key):
    base_url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GETDATASETLIST",
        "ResultFormat": "JSON"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            datasets = data["BEAAPI"]["Results"]["Dataset"]
            print("Available Datasets:")
            for dataset in datasets:
                print(f"- {dataset['DatasetName']}: {dataset['DatasetDescription']}")
        except KeyError:
            print("Failed to parse dataset list. Please check the API response structure.")
    else:
        print("Error fetching dataset list:", response.status_code)

api_key = os.getenv('BEA_API_KEY')
if not api_key:
    print("API key not found. Please set the BEA_API_KEY environment variable.")
    exit(1)

get_datasets(api_key)
