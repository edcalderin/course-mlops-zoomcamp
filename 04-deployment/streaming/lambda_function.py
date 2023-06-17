import base64
import boto3
import json
import mlflow
import os
import pickle

kinesis_client = boto3.client('kinesis')

PREDICTION_OUTPUT_STREAM_NAME= os.getenv('OUTPUT_STREAM_NAME')
RUN_ID = os.getenv('RUN_ID')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'
TRACKING_SERVER_HOST = 'ec2-3-145-45-64.us-east-2.compute.amazonaws.com'

PORT = 5000
mlflow.set_tracking_uri(f'http://{TRACKING_SERVER_HOST}:{PORT}')

def load_model(run_id: str):
    logged_model: str = f's3://mlflow-artifacts-erick/2/{run_id}/artifacts/model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    return loaded_model

def load_dictvectorizer(run_id:str):
    artifact_path = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path='artifacts/dv.pkl')
    with open(artifact_path, 'rb') as file:
        dv = pickle.load(file)
    return dv

def predict(features):
    model = load_model(RUN_ID)

    dv = load_dictvectorizer(RUN_ID)
    X = preprocess(features)
    X = dv.transform(features)
    print(f'{X=}')
    predictions = model.predict(X)

    return predictions[0]

def preprocess(features):
    PU_DO = features['PULocationID'] + '_' + features['DOLocationID']
    dicts = {'trip_distance': features['trip_distance'], 'PU_DO': PU_DO}
    return dicts

def predict(features):
    model = load_model(RUN_ID)
    dv = load_dictvectorizer(RUN_ID)

    X = preprocess(features)
    X = dv.transform(features)

    predictions = model.predict(X)
    return float(predictions[0])

def lambda_handler(event, context):

    predictions = []

    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')

        ride_event = json.loads(decoded_data)
        ride, ride_id = ride_event['ride'], ride_event['ride_id']

        prediction = predict(ride)

        prediction_event = {
            'model': 'ride_duration_prediction_model',
            'version': RUN_ID,
            'prediction': {
                'ride_duration': prediction,
                'ride_id': ride_id
            }
        }

        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTION_OUTPUT_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey='1'
            )
        predictions.append(prediction_event)

    return { 'predictions': predictions }
