FROM public.ecr.aws/lambda/python:3.10

RUN pip install --user --upgrade pip && pip install pipenv==2023.7.3

ENV PIPENV_IGNORE_VIRTUALENVS = 1

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY lambda_function.py model.py ./

CMD ["lambda_function.lambda_handler"]