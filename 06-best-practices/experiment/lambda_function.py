import model
import mlflow
import os

PREDICTION_OUTPUT_STREAM_NAME= os.getenv('OUTPUT_STREAM_NAME')
RUN_ID = os.getenv('RUN_ID')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'
TRACKING_SERVER_HOST = 'ec2-3-15-226-79.us-east-2.compute.amazonaws.com'
PORT = 5000
mlflow.set_tracking_uri(f'http://{TRACKING_SERVER_HOST}:{PORT}')

model_service = model.init(PREDICTION_OUTPUT_STREAM_NAME, RUN_ID, TEST_RUN)

def lambda_handler(event, context):
    return model_service.lambda_handler(event)
