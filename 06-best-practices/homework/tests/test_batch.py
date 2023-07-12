import pandas as pd
from pandas.testing import assert_frame_equal
from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)

data = [
    (None, None, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2), dt(1, 10)),
    (1, 2, dt(2, 2), dt(2, 3)),
    (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
    (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df = pd.DataFrame(data, columns=columns)

def prepare_data(df: pd.DataFrame)->pd.DataFrame:
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    categorical = ['PULocationID', 'DOLocationID']

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df

expected = pd.DataFrame([
    ('-1', '-1', dt(1, 2), dt(1, 10), 8.),
    ('1', '-1', dt(1, 2), dt(1, 10), 8.),
    ('1', '2', dt(2, 2), dt(2, 3), 1.)
], columns=columns+['duration'])

actual = prepare_data(df)

print(f'{expected =}')

assert_frame_equal(expected, actual)