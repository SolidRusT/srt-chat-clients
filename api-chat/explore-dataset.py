import requests
import os
import json

# Function to fetch available datasets
def fetch_datasets(api_key):
    url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GETDATASETLIST",
        "ResultFormat": "JSON"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        datasets = response.json()['BEAAPI']['Results']['Dataset']
        return datasets
    else:
        print("Error fetching datasets:", response.status_code)
        return None

# Function to fetch available parameters for a selected dataset
def fetch_dataset_parameters(api_key, dataset_name):
    url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GETPARAMETERLIST",
        "DataSetName": dataset_name,
        "ResultFormat": "JSON"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        parameters = response.json()['BEAAPI']['Results']['Parameter']
        return parameters
    else:
        print(f"Error fetching parameters for dataset {dataset_name}:", response.status_code)
        return None

# Function to explore available values for a selected parameter
def explore_parameter_values(api_key, dataset_name, parameter_name):
    url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GETPARAMETERVALUES",
        "DataSetName": dataset_name,
        "ParameterName": parameter_name,
        "ResultFormat": "JSON"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        values = response.json()['BEAAPI']['Results']['ParamValue']
        return values
    else:
        print(f"Error fetching values for parameter {parameter_name} in dataset {dataset_name}:", response.status_code)
        return None

# Main script
api_key = os.getenv('BEA_API_KEY')
if not api_key:
    print("API key not found. Please set the BEA_API_KEY environment variable.")
    exit(1)

print("Fetching available datasets...")
datasets = fetch_datasets(api_key)
if datasets:
    for dataset in datasets:
        print(f"- {dataset['DatasetName']}: {dataset['DatasetDescription']}")

dataset_name = input("\nEnter the dataset name you want to explore: ")
parameters = fetch_dataset_parameters(api_key, dataset_name)
if parameters:
    print(f"\nAvailable Parameters in {dataset_name}:")
    for parameter in parameters:
        print(f"- {parameter['ParameterName']}: {parameter['ParameterDescription']}")

parameter_name = input("\nEnter a parameter name to explore its values (or leave blank to skip): ")
if parameter_name:
    values = explore_parameter_values(api_key, dataset_name, parameter_name)
    if values:
        print(f"\nAvailable Values for {parameter_name} in {dataset_name}:")
        for value in values:
            print(f"- {value['Key']}: {value['Desc']}")
