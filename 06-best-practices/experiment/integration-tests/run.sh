#!bin/sh

LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`

export LOCAL_IMAGE_NAME=stream-model-duration:$LOCAL_TAG

cd "$(dirname "$0")"

docker build -t $LOCAL_IMAGE_NAME ..

docker-compose up -d

sleep 1

pipenv run python test-docker.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
fi

docker-compose down

exit ${ERROR_CODE}