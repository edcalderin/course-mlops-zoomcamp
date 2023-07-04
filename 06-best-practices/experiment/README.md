```bash
export AWS_PROFILE=mlflow-profile
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 345098143492.dkr.ecr.us-east-2.amazonaws.com

docker build -t stream-model-duration:v1 .

docker tag stream-model-duration:v1 345098143492.dkr.ecr.us-east-2.amazonaws.com/duration-model:v1
```

```bash
docker run -it --rm -p 8080:8080 \
 -e PREDICTIONS_STREAM_NAME="bla" \
 -e RUN_ID="77fb2593f2ad4558b83b7718643a8ed8" \
 -e TEST_RUN="True" \
 -e AWS_ACCESS_KEY_ID=AKIAVAWLTY4CMSI3TBG3 \
 -e AWS_SECRET_ACCESS_KEY=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 \
 -e AWS_DEFAULT_REGION="us-east-2" \
 stream-model-duration:v1
```