# course-mlops-zoomcamp
Repo to store homeworks.

Command to start MLFlow UI:
´mlflow ui --backend-store-uri sqlite:///02-experiment-tracking/mlflow.db´

prefect deploy 03-orchestration/orchestrate.py:main_flow -n 'homework-deployment' -p homework_pool