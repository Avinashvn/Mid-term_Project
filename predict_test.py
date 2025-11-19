# Import necessary libraries
import pickle
from flask import Flask, request, jsonify

## Load the model and DictVectorizer

with open("model_random_forest.bin", "rb") as f_in:
    dv, model = pickle.load(f_in)


# Create Flask app

app = Flask(__name__)


# Prediction endpoint

@app.route("/predict", methods=["POST"])
def predict():
    customer = request.get_json()

    # Convert customer dict into model input
    X = dv.transform([customer])

    # Predict (Random Forest outputs class label directly)
    y_pred = model.predict(X)[0]

    # Prepare readable response
    result = {
        "loan_eligible": bool(y_pred),
        "prediction": int(y_pred)
    }

    return jsonify(result)

# Start the Flask server
if __name__ == "__main__":
    print("Starting Flask server on port 9696...")
    app.run(debug=True, host="0.0.0.0", port=9696)
