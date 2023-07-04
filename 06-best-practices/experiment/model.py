import base64
import boto3
import json
import mlflow

kinesis_client = boto3.client('kinesis')

class ModelService:
    def __init__(self, model, test_run: bool, run_id: str) -> None:
        self.model = model
        self.test_run = test_run
        self.run_id = run_id

    def preprocess(self, ride):
        return {
            'PU_DO': f"{ride['PULocationID']}_{ride['DOLocationID']}",
            'trip_distance': ride['trip_distance']
        }

    def predict(self, features):
        predictions = self.model.predict(features)
        return float(predictions[0])

    def lambda_handler(self, event):

        predictions = []

        for record in event['Records']:
            encoded_data = record['kinesis']['data']

            ride_event = base64_decode(encoded_data)

            ride, ride_id = ride_event['ride'], ride_event['ride_id']
            X = self.preprocess(ride)

            prediction = self.predict(X)

            prediction_event = {
                'model': 'ride_duration_prediction_model',
                'version': self.run_id,
                'prediction': {
                    'ride_duration': prediction,
                    'ride_id': ride_id
                }
            }

            if not self.test_run:
                kinesis_client.put_record(
                    StreamName='PREDICTION_OUTPUT_STREAM_NAME',
                    Data=json.dumps(prediction_event),
                    PartitionKey='1'
                )
            predictions.append(prediction_event)

        return { 'predictions': predictions }

def load_model(run_id: str):
    logged_model: str = f's3://mlflow-artifacts-erick/1/{run_id}/artifacts/artifacts/model_mlflow'
    return mlflow.pyfunc.load_model(logged_model)

def init(run_id: str, test_run: str):
    model = load_model(run_id)
    return ModelService(model, test_run, run_id)

def base64_decode(encoded_data: str):
    decoded_data= base64.b64decode(encoded_data).decode('utf-8')
    ride_event = json.loads(decoded_data)
    return ride_event