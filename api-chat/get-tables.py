import requests
import os

def get_available_tables(api_key, dataset_name):
    """Fetch and display available tables or parameters for the specified dataset."""
    base_url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GetParameterValues",
        "DataSetName": dataset_name,
        "ParameterName": "TableName",  # Or adjust based on dataset requirements
        "ResultFormat": "JSON"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            if 'ParamValue' in data["BEAAPI"]["Results"]:
                print(f"Available Tables in {dataset_name}:")
                for item in data["BEAAPI"]["Results"]["ParamValue"]:
                    print(f"- {item['Key']}: {item['Desc']}")
            else:
                print(f"No tables found for {dataset_name}.")
        except KeyError:
            print("Failed to parse data. Please check your parameters.")
    else:
        print(f"Error fetching data: {response.status_code}")

def main():
    api_key = os.getenv('BEA_API_KEY')
    if not api_key:
        print("API key not found. Please set the BEA_API_KEY environment variable.")
        exit(1)
    
    dataset_name = input("Enter the dataset name: ")
    get_available_tables(api_key, dataset_name)

if __name__ == "__main__":
    main()
