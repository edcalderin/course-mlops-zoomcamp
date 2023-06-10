import requests

ride = {
    'PULocationID': 3,
    'DOLocationID': 2
}

URL = 'http://localhost:9696/predict'
response = requests.post(URL, json=ride)

print(response.json())