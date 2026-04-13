import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

print("Loading dataset...")
df = pd.read_csv("data/processed/final_features.csv")

# We ONLY want the explicit 15 features the dashboard uses
IMPORTANT_FEATURES = [
    "count_call", "count_delegatecall", "count_staticcall", "count_callcode",
    "count_sstore", "count_sload", "count_jump", "count_jumpi",
    "count_selfdestruct", "count_revert", "count_timestamp", "count_number", "count_blockhash",
    "count_add", "count_mul", "count_sub"
]

X = df[IMPORTANT_FEATURES]
y = df["vuln_type"]

df_bal = []
y_counts = y.value_counts()
print("Original classes:")
print(y_counts)

# Balance logic:
# 0 (block_dependency): 110 -> 1000
# 1 (ether_lock): 1365 -> 1000
# 2 (integer): 927 -> 1000
# 3 (reentrancy): 5431 -> 1000
target_size = 1000

for c in df["vuln_type"].unique():
    class_df = df[df["vuln_type"] == c]
    if len(class_df) < target_size:
        # Oversample
        resampled = class_df.sample(target_size, replace=True, random_state=42)
    else:
        # Undersample
        resampled = class_df.sample(target_size, replace=False, random_state=42)
    df_bal.append(resampled)

df_balanced = pd.concat(df_bal).reset_index(drop=True)

print("Balanced classes:")
print(df_balanced["vuln_type"].value_counts())

X_bal = df_balanced[IMPORTANT_FEATURES]
y_bal = df_balanced["vuln_type"]

X_train, X_test, y_train, y_test = train_test_split(
    X_bal, y_bal, test_size=0.2, stratify=y_bal, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

from sklearn.metrics import classification_report
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "models/rf_working_model.pkl")
print("Saved balanced RF model to models/rf_working_model.pkl")

# Test RF on minimal inputs
import numpy as np
# Empty
features0 = np.zeros((1, 13))
probs = model.predict_proba(features0)[0]
print("All Zeros:", model.classes_[np.argmax(probs)], "Conf:", np.max(probs))

# Ether Lock (Has CALL)
features_call = np.zeros((1, 13))
features_call[0][0] = 2 # count_call = 2
probs = model.predict_proba(features_call)[0]
print("Only CALL:", model.classes_[np.argmax(probs)], "Conf:", np.max(probs))

# Block Dependency (Has TIMESTAMP)
features_time = np.zeros((1, 13))
features_time[0][10] = 1 # count_timestamp = 1
probs = model.predict_proba(features_time)[0]
print("Only TIMESTAMP:", model.classes_[np.argmax(probs)], "Conf:", np.max(probs))

# Integer Overflow (Has neither CALL nor TIMESTAMP, but maybe has something else? Actually, RF might not predict Integer over empty because Integer has no features. Let's see.)
