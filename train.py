# Import necessary libraries
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier

# Parameters
data_file = "loan_data.csv"
model_file = "model_random_forest.bin"

# Load the dataset
df = pd.read_csv(data_file)
df["person_age"] = df["person_age"].astype("int")
df = df[df["person_age"] <= 80]

# Split the dataset
df_full_train, _df_test= train_test_split(df, test_size=0.2, random_state=1)

# Prepare the data
y_train = df_full_train["loan_status"].values  
y_test = _df_test["loan_status"].values

# Seperating categorical and numerical features
categorical_cols = df.select_dtypes(include=['object', 'category']).columns
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
numerical_cols = numerical_cols.drop('loan_status', errors='ignore')
feature_cols = list(categorical_cols) + list(numerical_cols)

# Vectorization
dv = DictVectorizer(sparse=False)   
train_dicts = df_full_train[feature_cols].to_dict(orient='records')
X_train = dv.fit_transform(train_dicts)
test_dicts = _df_test[feature_cols].to_dict(orient='records')
X_test = dv.transform(test_dicts)

# Train the model
print("Training the model...")
model = RandomForestClassifier(max_depth=15, min_samples_leaf=3,n_estimators=90, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test) 

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")  

# Save the model and vectorizer
with open(model_file, "wb") as f_out:   
    pickle.dump((dv, model), f_out)
print(f"Model and vectorizer saved to {model_file}")





