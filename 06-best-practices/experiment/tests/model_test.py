import lambda_function

def test_preprocess():
    ride = {
        "PULocationID": "23",
        "DOLocationID": "12",
        "trip_distance": 4
    }

    output = lambda_function.preprocess(ride)
    expected_features = {'trip_distance': 4, 'PU_DO': '23_12'}
    assert output==expected_features

def test_base64_decode():
    input = 'ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ=='
    output = lambda_function.base64_decode(input)
    expected_value = {
        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66
        },
        "ride_id": 256
    }

    assert output == expected_value

class ModelMock:
    def __init__(self, value) -> None:
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n

def test_predict():
    features = [{'trip_distance': 4, 'PU_DO': '23_12'}]
    model = ModelMock(10.0)
    predictions = lambda_function.predict(model, features)
    assert predictions == [10.0]