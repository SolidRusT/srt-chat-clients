import requests


# Function to make a generic request to the BEA API and return parsed JSON data
def query_bea_api(api_key, dataset, params):
    base_url = "https://apps.bea.gov/api/data"
    parameters = {
        "UserID": api_key,
        "method": "GetData",
        "DataSetName": dataset,
        "ResultFormat": "JSON",
        **params,
    }
    response = requests.get(base_url, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None


# Function to display the data
def display_data(data):
    try:
        # Navigate to the 'Results' section and then the 'Data' key
        results = data.get("BEAAPI", {}).get("Results", {})
        data_items = results.get("Data", [])

        # Check if 'Data' is found; if not, look for a more specific error message
        if not data_items:
            if "Error" in results:
                error_info = results["Error"]
                print(f"Error {error_info.get('APIErrorCode')}: {error_info.get('APIErrorDescription')}")
            else:
                print("No data found. Please check your parameters and try again.")
            return

        # If 'Data' is found, iterate and print each item
        for item in data_items:
            # Attempt to include a descriptive label for each data row
            description = item.get('LineDescription', 'Data Description Unavailable')
            value = item.get('DataValue', 'N/A')
            unit = item.get('CL_UNIT', '')
            period = item.get('TimePeriod', 'N/A')
            print(f"{description} ({period}): {value} {unit}")
    except KeyError as e:
        print("Unexpected structure in data. Missing key:", e)


# Main function to interact with the BEA API
def main():
    api_key = input("Enter your BEA API key: ")
    dataset = input("Enter the dataset name (e.g., 'NIPA', 'Regional'): ")
    params = {}
    while True:
        key = input("Enter parameter key (or 'done' to execute): ")
        if key.lower() == "done":
            break
        value = input(f"Enter value for {key}: ")
        params[key] = value

    data = query_bea_api(api_key, dataset, params)
    display_data(data)


if __name__ == "__main__":
    main()
