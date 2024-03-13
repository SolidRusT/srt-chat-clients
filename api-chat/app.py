import requests

# Function to get data from BEA API
def get_bea_data(api_key, dataset_name, year="2020", geo_fips="STATE"):
    base_url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GetData",
        "DataSetName": dataset_name,
        "Year": year,
        "GeoFIPS": geo_fips,
        "ResultFormat": "JSON"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Main CLI interface
def main():
    api_key = input("Enter your BEA API key: ")
    dataset_name = input("Enter the dataset name (e.g., 'NIPA'): ")
    year = input("Enter the year for the data (e.g., '2020'): ")
    geo_fips = input("Enter the geographic area (e.g., 'STATE' for all states): ")
    
    data = get_bea_data(api_key, dataset_name, year, geo_fips)
    if data:
        # Assuming the data structure, you'll need to adjust according to the actual API response
        for item in data['BEAAPI']['Results']['Data']:
            print(f"{item['GeoName']} ({item['TimePeriod']}): {item['DataValue']}")
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    main()
