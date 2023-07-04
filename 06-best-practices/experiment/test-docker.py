import requests

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
response = requests.post(URL, json=event)
print(response.json())