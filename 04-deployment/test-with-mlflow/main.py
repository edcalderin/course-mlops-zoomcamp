import pickle
from flask import Flask, request
import mlflow
import os

app = Flask('Duration-predictor')

mlflow.set_tracking_uri('http://127.0.0.1:5000')

RUN_ID = os.environ['RUN_ID']

def preprocess(features):
    PU_DO = features['PULocationID'] + '_' + features['DOLocationID']
    dicts = {'trip_distance':features['trip_distance'], 'PU_DO':PU_DO}
    return dicts

def load_model(run_id: str):
    logged_model: str = f'runs:/{run_id}/model'
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

@app.post('/predict')
def predict_endpoint():
    features = request.get_json()
    pred = predict(features)

    return {
        'duration': pred,
        'model_version': RUN_ID
    }