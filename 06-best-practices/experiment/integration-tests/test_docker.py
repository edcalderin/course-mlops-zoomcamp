#pylint: disable= duplicate-code
import requests
from deepdiff import DeepDiff

event = {
  "Records": [
    {
      "kinesis": {
        "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogIjIzIiwKICAgICAgICAgICAgIkRPTG9jYXRpb25JRCI6ICIxMiIsCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogNAogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiA1CiAgICB9",
      }
    }
  ]
}

URL = 'http://localhost:8080/2015-03-31/functions/function/invocations'
response = requests.post(URL, json=event, timeout=1).json()

RUN_ID = '77fb2593f2ad4558b83b7718643a8ed8'
RUN_ID = 'Test123'
expected = {
  'predictions':
    [
      {
        'model': 'ride_duration_prediction_model',
        'version': RUN_ID,
        'prediction': {
            'ride_duration': 20.002716357802516,
            'ride_id': 5
        }
      }
    ]
  }

diff = DeepDiff(response, expected, significant_digits=1)

print(f'{response=}')
print(f'{diff=}')

assert 'type_changes' not in diff
assert 'values_changed' not in diff
