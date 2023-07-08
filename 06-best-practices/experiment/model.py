import base64
import os
import json
import boto3
import mlflow

def get_model_location(run_id: str) -> str:
    model_location = os.getenv('MODEL_LOCATION')
    if model_location is not None:
        return model_location

    model_bucket = os.getenv('MODEL_BUCKET', 'mlflow-artifacts-erick')
    experiment_id = os.getenv('EXPERIMENT_ID', '1')

    logged_model: str = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts/artifacts/model_mlflow'
    return logged_model

def load_model(run_id: str):
    logged_model: str = get_model_location(run_id)
    return mlflow.pyfunc.load_model(logged_model)

class ModelService:
    def __init__(self, model, run_id: str, callbacks = None) -> None:
        self.model = model
        self.run_id = run_id
        self.callbacks = callbacks or []

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
            print(f'{prediction_event=}')
            for callback in self.callbacks:
                callback(prediction_event)

            predictions.append(prediction_event)

        return { 'predictions': predictions }

class KinesisCallback:

    def __init__(self, kinesis_client, prediction_output_stream: str) -> None:
        self.kinesis_client = kinesis_client
        self.prediction_output_stream = prediction_output_stream

    def put_record(self, prediction_event) -> None:
        self.kinesis_client.put_record(
            StreamName = self.prediction_output_stream,
            Data = json.dumps(prediction_event),
            PartitionKey='1'
        )

def create_kinesis_client():
    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')
    print(f'{endpoint_url=}')

    if endpoint_url is None:
        return boto3.client('kinesis')
    return boto3.client('kinesis', endpoint_url=endpoint_url)

def init(prediction_output_stream, run_id: str, test_run: bool):
    model = load_model(run_id)

    callbacks = []

    if not test_run:
        kinesis_client = create_kinesis_client()

        kinesis_callback = KinesisCallback(kinesis_client, prediction_output_stream)
        callbacks.append(kinesis_callback.put_record)

    return ModelService(model, run_id, callbacks)

def base64_decode(encoded_data: str):
    decoded_data= base64.b64decode(encoded_data).decode('utf-8')
    return json.loads(decoded_data)