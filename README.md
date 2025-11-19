# Mid-term_Project

This repository contains a loan default prediction model and a minimal web service to serve predictions.

- **Overview:**
- **Dataset:** `loan_data.csv` — raw dataset used for training.
- **Training script:** `train.py` — reads the CSV, trains a Random Forest classifier and a `DictVectorizer`, evaluates accuracy, and saves the model and vectorizer together in `model_random_forest.bin`.
- **Model files:** `model_random_forest.bin` — produced by `train.py` and used by the web service. This file contains a tuple `(dv, model)` pickled together.
- **Prediction service:** `predict_test.py` — Flask app that loads the vectorizer and model and exposes a `/predict` POST endpoint.
- **Client example:** `predict.py` — example script that posts a JSON customer record to the service and prints the response.
- **Notebook:** `notebook.ipynb` — exploratory analysis (optional).

This README explains how to set up the environment, run the training and service, and test predictions.

**Requirements**
- Python 3.8+ (you are using Python 3.13 — that should work but some packages may need compatible wheels)
- Install dependencies:
```
pip install -r requirements.txt
```
If `requirements.txt` is missing or incomplete, install the main packages:
```
pip install flask scikit-learn pandas requests
```

Alternatively you can use `pipenv` to create an isolated virtual environment and install the required packages there. This is the recommended approach for development because it keeps dependencies isolated from your system Python.

1. Install `pipenv` (system-wide or in a base environment):
```
pip install pipenv
```

2. Create a Pipenv environment using a specific Python version (choose a version you have installed, e.g. `3.8` or `3.13`):
```
pipenv --python 3.13
```

3. Install the project dependencies inside the Pipenv environment. This will add them to the generated `Pipfile`:
```
pipenv install pandas numpy scikit-learn flask waitress requests
```

4. Run commands inside the Pipenv environment:
- Start a shell inside the environment:
```
pipenv shell
```
- Or run a single command without entering the shell:
```
pipenv run python train.py
pipenv run python predict_test.py
```

Notes:
- `waitress` is recommended for serving the Flask app in production (on Windows/Linux). The `predict_test.py` script can be started under the Pipenv environment the same as shown above.
- The `Pipfile` created by `pipenv` records your dependencies; collaborators can run `pipenv install` to reproduce the environment.

**Train the model**
1. Make sure `loan_data.csv` is in the project root.
2. Run the training script:
```
python train.py
```
This will produce one file in the project root:
- `model_random_forest.bin` — a pickle containing `(dv, model)` where `dv` is the `DictVectorizer` and `model` is the trained Random Forest classifier.

**Run the prediction service**
1. Start the Flask app (from the project root):
```
python predict_test.py
```
By default the app runs on `http://0.0.0.0:9696` (port 9696). If you prefer `flask run` you can:
```
set FLASK_APP=predict_test.py
flask run --port 9696
```

2. Confirm the server is listening (optional):
```
netstat -ano | findstr :9696
```

**Test the service**
- Use the example client `predict.py`:
```
python predict.py
```
- Or with `curl`:
```
curl -X POST http://localhost:9696/predict -H "Content-Type: application/json" -d "{ \"person_age\": 30, \"person_gender\": \"female\", ... }"
```

**Common issues & troubleshooting**
- Connection refused (WinError 10061): means the client couldn't reach the server. Fixes:
	- Start `predict_test.py` so the Flask server is running.
	- Verify the server didn't crash on startup due to missing files or package errors — run `python predict_test.py` and inspect the console for tracebacks.
	- Ensure the client uses the same host/port (`http://localhost:9696/predict`).
	- Check `netstat` to see whether a process is listening on port 9696.
- FileNotFoundError for `model_random_forest.bin`: run `train.py` first or copy the model file into the project root. The `model_random_forest.bin` file contains both the vectorizer and the model.
- ModuleNotFoundError when starting server: install the missing package with `pip`.

**Notes about code**
- `train.py` trains a Random Forest classifier and uses `DictVectorizer` to transform rows into feature vectors. It saves the vectorizer and model together with `pickle` into `model_random_forest.bin`.
- `predict_test.py` expects the vectorizer to accept a dict with the same keys as produced by the training data (column names). It returns JSON: `{ "loan_eligible": true|false, "prediction": 0|1 }`.
- `predict.py` posts a sample customer JSON and prints the returned prediction.


**Docker (build & run)**
The project contains a `Dockerfile` but it expects model files to be available inside the image. There are two common ways to run the service with Docker:

1) Build an image that contains the model files (bakes files into the image)

-- Make sure `model_random_forest.bin` is present in the project root, or update the `Dockerfile` to copy the correct filename(s).
-- Example `Dockerfile` changes (copy the combined pickle into the image):
```
COPY model_random_forest.bin ./
```
- Build the image:
```
docker build -t loan-predictor:latest .
```
- Run the container (expose port 9696):
```
docker run --rm -p 9696:9696 loan-predictor:latest
```

2) Run the official `Dockerfile` but mount model files at runtime (recommended during development)

- Build the image (no model files baked in):
```
docker build -t loan-predictor:dev .
```
-- Run the container and bind-mount your model files and project directory so the container can load them from `/app`:
```
docker run --rm -p 9696:9696 -v "%CD%:/app" loan-predictor:dev
```
On Windows `cmd.exe` the `"%CD%"` expands to the current directory. This mounts your project (including `model_random_forest.bin`) into `/app` inside the container so `predict_test.py` can open it.

Notes:
- If you use Docker on Linux/macOS, replace `"%CD%"` with `$(pwd)`.
- If your Dockerfile uses different filenames, either update the Dockerfile or use the bind-mount approach.
- After the container starts, call the endpoint at `http://localhost:9696/predict` (same as local development).

