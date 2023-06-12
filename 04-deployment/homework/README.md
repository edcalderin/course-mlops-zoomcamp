# Homework 4

## Steps to reproduce with Docker

1. `docker build -t homework-04 .`
2. `docker run -e AWS_ACCESS_KEY_ID=xxxxxxxx -e AWS_SECRET_ACCESS_KEY=xxxxxx -it homework-04`

 Expected output:
```
Reading data...
Mean predicted duration 12.76941328837231
Uploading to S3...
Uploaded to S3!
```