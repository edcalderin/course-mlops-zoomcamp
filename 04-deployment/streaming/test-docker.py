import requests

event = {
  "Records": [
    {
      "kinesis": {
        "kinesisSchemaVersion": "1.0",
        "partitionKey": "1",
        "sequenceNumber": "49641758460084567267101086389911957362585961512447246338",
        "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogIjIzIiwKICAgICAgICAgICAgIkRPTG9jYXRpb25JRCI6ICIxMiIsCiAgICAgICAgICAgICJ0cmlwX2Rpc3RhbmNlIjogNAogICAgICAgIH0sCiAgICAgICAgInJpZGVfaWQiOiA1CiAgICB9",
        "approximateArrivalTimestamp": 1686927244.188
      },
      "eventSource": "aws:kinesis",
      "eventVersion": "1.0",
      "eventID": "shardId-000000000000:49641758460084567267101086389911957362585961512447246338",
      "eventName": "aws:kinesis:record",
      "invokeIdentityArn": "arn:aws:iam::xxx:role/lambda-kinesis-role",
      "awsRegion": "us-east-2",
      "eventSourceARN": "arn:aws:kinesis:us-east-2:xxx:stream/ride_events"
    }
  ]
}

URL = 'http://localhost:8080/2015-03-31/functions/function/invocations'
response = requests.post(URL, json=event)
print(response.json())