import requests

ride = {
    'PULocationID': '116',
    'DOLocationID': '200',
    'trip_distance': 23
}

URL = 'http://localhost:9696/predict'
response = requests.post(URL, json=ride)

print(response.json())