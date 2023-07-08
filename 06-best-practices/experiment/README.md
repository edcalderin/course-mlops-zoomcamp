# Code snippets

## Building images to ECR

```bash
export AWS_PROFILE=mlflow-profile
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin xxx.dkr.ecr.us-east-2.amazonaws.com

docker build -t stream-model-duration:v1 .

docker tag stream-model-duration:v1 xxx.dkr.ecr.us-east-2.amazonaws.com/duration-model:v1
```

## Running image locally

```bash
docker run -it --rm \
 -p 8080:8080 \
 -e PREDICTIONS_STREAM_NAME="bla" \
 -e RUN_ID="Test123" \
 -e TEST_RUN="True" \
 -e MODEL_LOCATION="/app/model" \
 -e AWS_ACCESS_KEY_ID=xxx \
 -e AWS_SECRET_ACCESS_KEY=xxx \
 -e AWS_DEFAULT_REGION="us-east-2" \
 -v "C:\Users\Erick\Projects\course-mlops-zoomcamp\06-best-practices\experiment\integration-tests\model:/app/model" \
 stream-model-duration:v1
```

## Run integration tests

sh ./integration-tests/run.sh

## Activate pipenv manually

```bash
source $(pipenv --venv)/Scripts/activate
```

## Localstack

### Creating awslocal command

```bash
export awslocal="AWS_ACCESS_KEY_ID=abc AWS_SECRET_ACCESS_KEY=xyz AWS_DEFAULT_REGION=us-east-2 aws --endpoint-url=http://127.0.0.1:4566"
```

### List streams
```bash
awslocal kinesis list-streams
```

```bash
awslocal kinesis create-stream \
    --stream-name ride-predictions \
    --shard-count 1
```

## Reading from the stream

```bash
export KINESIS_STREAM_OUTPUT=ride_predictions
export SHARD='shardId-000000000000'

SHARD_ITERATOR=$(awslocal kinesis get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator'
)

RESULT=$(awslocal kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode

