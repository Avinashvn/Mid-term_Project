# Import necessary libraries
import requests
import json

url = "http://localhost:9696/predict"

customer_id = "xyz-456"
customer = {
    "person_age": 32,
    "person_gender": "male",
    "person_education": "Bachelor",
    "person_income": 48000.0,
    "person_emp_exp": 6,
    "person_home_ownership": "RENT",
    "loan_amnt": 12000.0,
    "loan_intent": "EDUCATION",
    "loan_int_rate": 9.8,
    "loan_percent_income": 0.25,
    "cb_person_cred_hist_length": 7.0,
    "credit_score": 678,
    "previous_loan_defaults_on_file": "Yes",
}

response = requests.post(url, json=customer)

if response.status_code == 200:
    print("Prediction:", response.json())
else:
    print("Request failed with status:", response.status_code)
    print("Message:", response.text)

