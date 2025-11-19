# Mid-term_Project

This repository contains a loan default prediction model and a minimal web service to serve predictions.

**Overview:**
- **Dataset:** `loan_data.csv` — raw dataset used for training.
- **Training script:** `train.py` — reads the CSV, trains an XGBoost classifier and a `DictVectorizer`, evaluates AUC, and saves the model (`xgbcmodel.bin`) and vectorizer (`dv.bin`).
- **Model files:** `xgbcmodel.bin`, `dv.bin` — produced by `train.py` and used by the web service.
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
pip install flask xgboost scikit-learn pandas requests
```

**Train the model**
1. Make sure `loan_data.csv` is in the project root.
2. Run the training script:
```
python train.py
```
This will produce two files in the project root:
- `xgbcmodel.bin` — the trained XGBoost model (pickle)
- `dv.bin` — the `DictVectorizer` used to transform input dicts into model features

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
- FileNotFoundError for `xgbcmodel.bin` / `dv.bin`: run `train.py` first or copy the model files into the project root.
- ModuleNotFoundError when starting server: install the missing package with `pip`.

**Notes about code**
- `train.py` trains an XGBoost classifier and uses `DictVectorizer` to transform rows into feature vectors. It saves the model and vectorizer with `pickle`.
- `predict_test.py` expects the vectorizer to accept a dict with the same keys as produced by the training data (column names). It returns JSON: `{ "loan_status": 0|1, "probability": <float> }`.
- `predict.py` posts a sample customer JSON and prints the returned prediction.


**Docker (build & run)**
The project contains a `Dockerfile` but it expects model files to be available inside the image. There are two common ways to run the service with Docker:

1) Build an image that contains the model files (bakes files into the image)

- Make sure `xgbcmodel.bin` and `dv.bin` are present in the project root, or update the `Dockerfile` to copy the correct filenames.
- Example `Dockerfile` changes (replace `model_random_forest.bin` with the actual files):
```
COPY xgbcmodel.bin dv.bin ./
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
- Run the container and bind-mount your model files and project directory so the container can load them from `/app`:
```
docker run --rm -p 9696:9696 -v "%CD%:/app" loan-predictor:dev
```
On Windows `cmd.exe` the `"%CD%"` expands to the current directory. This mounts your project (including `xgbcmodel.bin` and `dv.bin`) into `/app` inside the container so `predict_test.py` can open them.

Notes:
- If you use Docker on Linux/macOS, replace `"%CD%"` with `$(pwd)`.
- If your Dockerfile uses different filenames, either update the Dockerfile or use the bind-mount approach.
- After the container starts, call the endpoint at `http://localhost:9696/predict` (same as local development).

If you want, I can:
- Add more detailed API docs (example request body schema).
- Create a `requirements.txt` with pinned versions.
- Help you create a Docker image and example `docker run` commands.

---

If you want me to adjust the README text (format, add examples or change port), tell me what to include and I'll update it.

