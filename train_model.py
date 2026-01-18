import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from features import extract_features # Imports the function from features.py

# Loads data from CSV
print("Loading dataset...")
df = pd.read_csv('malicious_phish.csv') 

# Preprocessing - 'benign' is 0, everything else (phishing, malware) is 1
df['label'] = df['type'].apply(lambda x: 0 if x == 'benign' else 1)

# Applies feature extraction
print("Extracting features... this may take a moment.")
features_list = df['url'].apply(lambda x: list(extract_features(x).values()))

# Converts features to DataFrame for training
X = pd.DataFrame(features_list.tolist())
y = df['label']

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Trains model
print("Training Random Forest...")
rf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
rf.fit(X_train, y_train)

# Evaluates data
print("Evaluating...")
preds = rf.predict(X_test)
print(classification_report(y_test, preds))

# Saves the model
joblib.dump(rf, 'malicious_url_model.pkl')
print("Model saved!")