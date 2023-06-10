import pickle
from flask import Flask, request

FILE_NAME = "lin_reg.bin"

app = Flask('Duraction-predictor')

with open(FILE_NAME, 'rb') as file:
    dv, lr_model = pickle.load(file)

def predict(features):
    X = dv.transform(features)
    predictions = lr_model.predict(X)
    return predictions[0]

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    features = request.get_json()

    pred = predict(features)

    return {
        'duration': pred
    }
