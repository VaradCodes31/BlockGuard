import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("data/processed/final_features.csv")
IMPORTANT_FEATURES = [
    "count_call", "count_delegatecall", "count_staticcall", "count_callcode",
    "count_sstore", "count_sload", "count_jump", "count_jumpi",
    "count_selfdestruct", "count_revert", "count_timestamp", "count_number", "count_blockhash",
    "count_add", "count_mul", "count_sub"
]

X = df[IMPORTANT_FEATURES]
y = df["vuln_type"]

# Balance the dataset completely perfectly
df_bal = []
target_size = 1000
for c in df["vuln_type"].unique():
    class_df = df[df["vuln_type"] == c]
    if len(class_df) < target_size:
        resampled = class_df.sample(target_size, replace=True, random_state=42)
    else:
        resampled = class_df.sample(target_size, replace=False, random_state=42)
    df_bal.append(resampled)

df_balanced = pd.concat(df_bal).reset_index(drop=True)
X_bal = df_balanced[IMPORTANT_FEATURES]
y_bal = df_balanced["vuln_type"]

nb_model = MultinomialNB()
nb_model.fit(X_bal, y_bal)

print("Validation on original dataset:")
print(classification_report(y, nb_model.predict(X)))

print("\n--- Testing Edge Cases ---")
def test_snippet(name, counts):
    features = np.zeros((1, 16))
    for i, count in counts.items():
        features[0][i] = count
    probs = nb_model.predict_proba(features)[0]
    pred_class_idx = np.argmax(probs)
    label = nb_model.classes_[pred_class_idx]
    print(f"{name}: {label} (Conf: {probs[pred_class_idx]:.3f})")

test_snippet("Integer Overflow (ADD, MUL, SSTORE)", {13: 1, 14: 1, 4: 1})
test_snippet("Ether Lock (CALL)", {0: 1})
test_snippet("Ether Lock (CALL, SSTORE)", {0: 1, 4: 1})
test_snippet("Block Dependency (TIMESTAMP)", {10: 1})
test_snippet("Reentrancy (CALL, SSTORE, ADD)", {0: 1, 4: 1, 13: 1})
test_snippet("Reentrancy (CALL)", {0: 1})

joblib.dump(nb_model, "models/nb_model.pkl")
