import joblib
import numpy as np

# Load the RF model
rf_model = joblib.load('models/rf_working_model.pkl')

# Our 16 features:
# CALL, DELEGATECALL, STATICCALL, CALLCODE, SSTORE, SLOAD, JUMP, JUMPI, SELFDESTRUCT, REVERT, TIMESTAMP, NUMBER, BLOCKHASH, ADD, MUL, SUB

def test_snippet(name, counts):
    # Initialize 16 zeros
    features = np.zeros((1, 16))
    for i, count in counts.items():
        features[0][i] = count
    
    probs = rf_model.predict_proba(features)[0]
    pred_class_idx = np.argmax(probs)
    label = rf_model.classes_[pred_class_idx]
    
    print(f"\nSnippet: {name}")
    print(f"Prediction: {label} (Conf: {probs[pred_class_idx]:.3f})")

# Integer Overflow snippet (e.g. ADD MUL SSTORE) -> indices: ADD=13, MUL=14, SSTORE=4
test_snippet("Integer Overflow (ADD, MUL, SSTORE)", {13: 1, 14: 1, 4: 1})

# Ether Lock snippet (e.g. CALL VALUE BALANCE) -> indices: CALL=0
# Value and Balance are not explicitly tracked in features! Only CALL!
test_snippet("Ether Lock (CALL)", {0: 1})

# Ether Lock 2 (CALL, SSTORE) -> CALL=0, SSTORE=4
test_snippet("Ether Lock (CALL, SSTORE)", {0: 1, 4: 1})

# Block Dependency (TIMESTAMP) -> TIMESTAMP=10
test_snippet("Block Dependency (TIMESTAMP)", {10: 1})
