FROM public.ecr.aws/lambda/python:3.9

COPY . .

RUN pip install -U pip
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]