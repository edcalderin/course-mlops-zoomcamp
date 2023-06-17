# Helpers

## Putting records
```bash
KINESIS_STREAM_INPUT='ride_events'

aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --cli-binary-format raw-in-base64-out \
    --data '{
        "ride": {
            "PULocationID": "23",
            "DOLocationID": "12",
            "trip_distance": 4
        },
        "ride_id": 125
    }'
```

## Reading from the stream

```bash
KINESIS_STREAM_OUTPUT=ride_predictions
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode
```
## Test run with python script

```bash
export OUTPUT_STREAM_NAME=ride_predictions
export RUN_ID='7059c0d3f6894cffba900268742fce14'
export TEST_RUN='True'
```

## Running image
```bash
docker build -t stream-model-duration:v1 .

docker run -it --rm -p 8080:8080 \
    -e OUTPUT_STREAM_NAME=ride_predictions \
    -e RUN_ID='7059c0d3f6894cffba900268742fce14' \
    -e TEST_RUN='True' \
    -e AWS_DEFAULT_REGION='us-east-2' \
    -e AWS_ACCESS_KEY_ID='XXXXX'\
    -e AWS_SECRET_ACCESS_KEY='XXXXX'\
    stream-model-duration:v1
```
In a separate terminal, you can then locally invoke the function using cURL:

`curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'`

## Pushing image to ECR

```bash
export AWS_PROFILE=mlflow-profile
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 345098143492.dkr.ecr.us-east-2.amazonaws.com

docker build -t stream-model-duration:v1 .

docker tag stream-model-duration:v1 345098143492.dkr.ecr.us-east-2.amazonaws.com/duration-model:v1

docker push 345098143492.dkr.ecr.us-east-2.amazonaws.com/duration-model:v1

```