import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load the Iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

# Instantiate and train your logistic regression model
lr = LogisticRegression()
lr.fit(X_train, y_train)

# Set our tracking server uri for logging
mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# Create a new MLflow Experiment
mlflow.set_experiment("MLflow Quickstart")

# Placeholder for accuracy calculation (replace this with actual calculation)
accuracy = 0.85

params = {
    "solver": "lbfgs",
    "max_iter": 1200,
    "multi_class": "auto",
    "random_state": 8888,
}

# Start an MLflow run
with mlflow.start_run():
    # Log the hyperparameters
    mlflow.log_params(params)

    # Log the loss metric (assuming accuracy is calculated elsewhere)
    mlflow.log_metric("accuracy", accuracy)

    # Set a tag that we can use to remind ourselves what this run was for
    mlflow.set_tag("Training Info", "Basic LR model for iris data")

    # Log the model
    model_info = mlflow.sklearn.log_model(
        sk_model=lr,
        artifact_path="iris_model",
        input_example=X_train,  # Assuming X_train is defined elsewhere
        registered_model_name="tracking-quickstart",
    )
