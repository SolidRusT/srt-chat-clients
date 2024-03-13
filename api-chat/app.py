import requests

# Function to make a generic request to the BEA API and return parsed JSON data
def query_bea_api(api_key, dataset, params):
    base_url = "https://apps.bea.gov/api/data"
    parameters = {
        "UserID": api_key,
        "method": "GetData",
        "DataSetName": dataset,
        "ResultFormat": "JSON",
        **params
    }
    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None

# Function to display the data
def display_data(data):
    if data:
        try:
            for item in data["BEAAPI"]["Results"]["Data"]:
                print(f"{item['GeoName']} ({item['TimePeriod']}): {item['DataValue']} {item.get('CL_UNIT', '')}")
        except KeyError as e:
            print("Failed to parse data. Missing key:", e)

# Main function to interact with the BEA API
def main():
    api_key = input("Enter your BEA API key: ")
    dataset = input("Enter the dataset name (e.g., 'NIPA', 'Regional'): ")
    params = {}
    while True:
        key = input("Enter parameter key (or 'done' to execute): ")
        if key.lower() == 'done':
            break
        value = input(f"Enter value for {key}: ")
        params[key] = value

    data = query_bea_api(api_key, dataset, params)
    display_data(data)

if __name__ == "__main__":
    main()
