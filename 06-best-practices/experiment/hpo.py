import os
import pickle
import click
import mlflow
import optuna
import pandas as pd
from optuna.samplers import TPESampler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error

os.environ['AWS_PROFILE'] = 'mlflow-profile'
TRACKING_SERVER_HOST = 'ec2-3-15-226-79.us-east-2.compute.amazonaws.com'
PORT = 5000
mlflow.set_tracking_uri(f'http://{TRACKING_SERVER_HOST}:{PORT}')
mlflow.set_experiment("random-forest-optuna2")


def load_pickle(filename):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    return df

def prepare_dictionaries(df: pd.DataFrame):
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts

@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--num_trials",
    default=1,
    help="The number of parameter evaluations for the optimizer to explore"
)
def run_optimization(num_trials: int=None):

    df_train = read_dataframe('data/green/green_tripdata_2022-01.parquet')
    X_train = prepare_dictionaries(df_train.drop('duration', axis=1))
    y_train = df_train['duration']

    df_val = read_dataframe('data/green/green_tripdata_2022-02.parquet')
    X_val = prepare_dictionaries(df_val.drop('duration', axis=1))
    y_val = df_val['duration']

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 10, 50, 1),
            'max_depth': trial.suggest_int('max_depth', 1, 20, 1),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10, 1),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 4, 1),
            'random_state': 42,
            'n_jobs': -1
        }
        with mlflow.start_run():
            mlflow.set_tag('model', 'RandomForestRegressor')
            mlflow.log_params(params)

            pipeline = make_pipeline(
                DictVectorizer(),
                RandomForestRegressor(**params)
            )
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_val)

            rmse = mean_squared_error(y_val, y_pred, squared=False)

            mlflow.log_metric('rmse', rmse)
            mlflow.sklearn.log_model(pipeline, artifact_path='artifacts/model_mlflow')

            return rmse

    sampler = TPESampler(seed=42)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=num_trials)


if __name__ == '__main__':
    run_optimization()
