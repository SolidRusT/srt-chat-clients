import os
import requests

def get_parameter_values(api_key, dataset_name, parameter_name):
    base_url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GetParameterValues",
        "DataSetName": dataset_name,
        "ParameterName": parameter_name,
        "ResultFormat": "JSON"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            if 'ParamValue' in data["BEAAPI"]["Results"]:
                for item in data["BEAAPI"]["Results"]["ParamValue"]:
                    print(f"Code: {item['Key']}, Description: {item['Desc']}")
            else:
                print(f"No parameter values found for {parameter_name} in {dataset_name}.")
        except KeyError:
            print("Failed to parse data. Please check your parameters.")
    else:
        print("Error fetching data:", response.status_code)

api_key = os.getenv('BEA_API_KEY')
if not api_key:
    print("API key not found. Please set the BEA_API_KEY environment variable.")
    exit(1)

dataset_name = input("Enter the dataset name (e.g., 'Regional', 'NIPA', 'NIUnderlyingDetail'): ")
parameter_name = input("Enter the parameter name (e.g., 'TableName', 'LineCode'): ")

get_parameter_values(api_key, dataset_name, parameter_name)
