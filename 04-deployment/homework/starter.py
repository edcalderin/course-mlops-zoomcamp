
import os
import pandas as pd
import pickle
import sys

def load_artifacts():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

def read_data(filename: str, categorical_columns):
    print('Reading data...')

    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical_columns] = df[categorical_columns].fillna(-1).astype('int').astype('str')

    return df

def prepare_predictions(df: pd.DataFrame, categorical_columns, year: int, month: int):
    dicts = df[categorical_columns].to_dict(orient='records')

    dv, model = load_artifacts()

    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    return pd.DataFrame({'ride_id': df['ride_id'], 'predictions': y_pred})

def upload_to_s3(df: pd.DataFrame, year: int, month: int):
    output_file = f's3://mlops-outputs/04-homework/predictions_{year}_{month:02d}.parquet'

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    print('Uploading to S3...')

    df.to_parquet(
        output_file,
        storage_options={
            "key": AWS_ACCESS_KEY_ID,
            "secret": AWS_SECRET_ACCESS_KEY,
        },
        engine='pyarrow',
        compression=None,
        index=False
    )

    print('Uploaded to S3!')

def main():

    year, month = int(sys.argv[1]), int(sys.argv[2])

    categorical = ['PULocationID', 'DOLocationID']

    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet', categorical)

    df = prepare_predictions(df, categorical, year, month)

    print('Mean predicted duration', df.predictions.mean())

    upload_to_s3(df, year, month)

main()