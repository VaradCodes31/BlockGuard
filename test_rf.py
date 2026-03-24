import pandas as pd
import joblib
import numpy as np

# Let's check the mean values for all features in the dataset per class
df = pd.read_csv("data/processed/final_features.csv")
print("----- Dataset Means -----")
print(df.groupby('vuln_type').mean().T)

print("\n----- Testing RF with zeros and low counts -----")
rf_model = joblib.load('models/rf_working_model.pkl')
features0 = np.zeros((1, 15))
probs = rf_model.predict_proba(features0)[0]
print("All Zeros:", rf_model.classes_[np.argmax(probs)], "Conf:", np.max(probs))

features_call = np.zeros((1, 15))
features_call[0][2] = 1 # count_call = 1
probs = rf_model.predict_proba(features_call)[0]
print("Only CALL:", rf_model.classes_[np.argmax(probs)], "Conf:", np.max(probs))

features_sload = np.zeros((1, 15))
features_sload[0][7] = 1 # count_sload = 1
probs = rf_model.predict_proba(features_sload)[0]
print("Only SLOAD:", rf_model.classes_[np.argmax(probs)], "Conf:", np.max(probs))
