# pylint: disable= duplicate-code
import os
import json

import boto3
from deepdiff import DeepDiff

kinesis_stream_name = os.getenv('KINESIS_STREAM_NAME', 'ride_predictions')
kinesis_endpoint = os.getenv('KINESIS_ENDPOINT_URL', 'http://localhost:4566')

kinesis_client = boto3.client('kinesis', endpoint_url=kinesis_endpoint)

SHARD_ID = 'shardId-000000000000'

shard_iterator = kinesis_client.get_shard_iterator(
    StreamName=kinesis_stream_name,
    ShardId=SHARD_ID,
    ShardIteratorType='TRIM_HORIZON',
)

result = kinesis_client.get_records(ShardIterator=shard_iterator['ShardIterator'])

response = result['Records']

assert len(response) == 1, 'Lenght does not match'

response = json.loads(response[0]['Data'])

expected = {
    'model': 'ride_duration_prediction_model',
    'version': 'Test123',
    'prediction': {
        'ride_duration': 20.002716357802516,
        'ride_id': 5,
    },
}

diff = DeepDiff(response, expected, significant_digits=1)

print(f'{response=}')
print(f'{diff=}')

assert 'type_changes' not in diff
assert 'values_changed' not in diff
