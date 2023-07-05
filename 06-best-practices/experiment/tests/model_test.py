import model

def test_preprocess():
    ride = {
        "PULocationID": "23",
        "DOLocationID": "12",
        "trip_distance": 4
    }

    expected_features = {'trip_distance': 4, 'PU_DO': '23_12'}
    model_service = model.ModelService(None, True, None)
    output = model_service.preprocess(ride)
    assert output==expected_features

def test_base64_decode():
    input = 'ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ=='
    output = model.base64_decode(input)
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
    model_mock = ModelMock(10.0)
    model_service = model.ModelService(model_mock, True, '')
    predictions = model_service.predict(features)
    assert predictions == 10.0

def test_lambda_handler():
    EVENT = {
        "Records": [
            {
                "kinesis": {
                    "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogIjIzIiwKICAgICAgICAgICAgIkRPTG9jYXRpb25JRCI6ICIxMiIsCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogNAogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiA1CiAgICB9",
                }
            }
        ]
    }
    RUN_ID: str = '123'
    expected = {
        'predictions':
            [
                {
                    'model': 'ride_duration_prediction_model',
                    'version': RUN_ID,
                    'prediction': {
                        'ride_duration': 10.0,
                        'ride_id': 5
                    }
                }
            ]
    }

    model_mock = ModelMock(10.0)
    model_service = model.ModelService(model_mock, True, RUN_ID)
    output = model_service.lambda_handler(EVENT)
    assert output == expected