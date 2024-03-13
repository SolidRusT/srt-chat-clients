import requests

def get_parameter_values(api_key):
    base_url = "https://apps.bea.gov/api/data"
    params = {
        "UserID": api_key,
        "method": "GetParameterValues",
        "DataSetName": "Regional",
        "ParameterName": "TableName",
        "ResultFormat": "JSON"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            for item in data["BEAAPI"]["Results"]["ParamValue"]:
                print(f"Code: {item['Key']}, Description: {item['Desc']}")
        except KeyError:
            print("Failed to parse data. Please check your parameters.")
    else:
        print("Error fetching data:", response.status_code)

api_key = "<your_api_key_here>"  # Replace <your_api_key_here> with your actual API key
get_parameter_values(api_key)
