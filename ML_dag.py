from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mlflow_sklearn_iris',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
)

def load_data():
    global X_train, X_test, y_train, y_test
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

def train_model():
    global lr
    lr = LogisticRegression()
    lr.fit(X_train, y_train)

def log_results():
    mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
    mlflow.set_experiment("MLflow Quickstart")

    accuracy = lr.score(X_test, y_test)
    params = {
        "solver": "lbfgs",
        "max_iter": 1200,
        "multi_class": "auto",
        "random_state": 8888,
    }

    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.set_tag("Training Info", "Basic LR model for iris data")
        mlflow.sklearn.log_model(
            sk_model=lr,
            artifact_path="iris_model",
            input_example=X_train,
            registered_model_name="tracking-quickstart",
        )

def make_predictions():
    global predictions
    predictions = lr.predict(X_test)
    print("Predictions:", predictions)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

log_results_task = PythonOperator(
    task_id='log_results',
    python_callable=log_results,
    dag=dag,
)

make_predictions_task = PythonOperator(
    task_id='make_predictions',
    python_callable=make_predictions,
    dag=dag,
)


# Set the dependencies between the tasks
load_data_task >> train_model_task >> log_results_task >> make_predictions_task
