import requests
import config

# Get the dataset from Rebase Energy dataset API
def get_data(name, asset):
    print("Getting dataset:", name)
    url = f"{config.HOST_NAME}/api/v1/datasets/{name}"
    params = {
        'asset': asset
    }
    resp = requests.get(url, params=params)
    print("API status code:", resp.status_code)
    resp.raise_for_status()
    return resp.json()