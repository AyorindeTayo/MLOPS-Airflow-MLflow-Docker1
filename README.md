
# Installing dependencies 
- cd /path/to/project-directory      # Choose your project directory
```
conda create -n env1 python
```
Then, activate this app's virtualenv: virtualenv -p python3 venv1  # For Python 3
```
conda activate env1
```

- Install your requirements
```
(venv)$ pip install -r requirements.txt
```
- install dependencies packages 
```
pip install mlflow
```
```
pip install pandas
```
# Run tracking server locally 
```
mlflow server --host 127.0.0.1 --port 8080
```
- 4 runs was carried out by varrying the hyperparameters
![Imgur](https://imgur.com/BWyZW40.jpg)
