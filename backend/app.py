import os
import sys
import pickle
import numpy as np
import tensorflow as tf
from collections import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shap
import joblib

app = Flask(__name__)
# Enable CORS for all origins (allows React dev server on 5173 to contact Flask on 5000)
CORS(app)

# -------------------------------
# Path Setup Helper (Mirroring Streamlit)
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DL_DIR = os.path.join(BASE_DIR, "deep_learning")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Append feature engineering to sys.path so we can import opcode_extractor
sys.path.append(os.path.join(BASE_DIR, "feature_engineering"))
from opcode_extractor import bytecode_to_opcodes

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# -------------------------------
# Load Global Models
# -------------------------------
print("Loading Models...")
MODEL_PATH = os.path.join(DL_DIR, "blockguard_opcode_model.h5")
TOKENIZER_PATH = os.path.join(DL_DIR, "tokenizer.pkl")
LABEL_ENCODER_PATH = os.path.join(DL_DIR, "label_encoder.pkl")
RF_MODEL_PATH = os.path.join(MODEL_DIR, "rf_working_model.pkl")

# Keras / Transformers / Sklearn
blockguard_model = load_model(MODEL_PATH)
rf_model = joblib.load(RF_MODEL_PATH)

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

MAX_LEN = 500
print("Models loaded successfully.")

# -------------------------------
# Feature Extraction (Machine Learning Router)
# -------------------------------
def extract_features_from_opcodes(opcodes):
    freq = Counter(opcodes)
    total = sum(freq.values())

    features = {
        "count_call": freq.get("CALL", 0),
        "count_delegatecall": freq.get("DELEGATECALL", 0),
        "count_staticcall": freq.get("STATICCALL", 0),
        "count_callcode": freq.get("CALLCODE", 0),
        "count_sstore": freq.get("SSTORE", 0),
        "count_sload": freq.get("SLOAD", 0),
        "count_jump": freq.get("JUMP", 0),
        "count_jumpi": freq.get("JUMPI", 0),
        "count_selfdestruct": freq.get("SELFDESTRUCT", 0),
        "count_revert": freq.get("REVERT", 0),
        "count_timestamp": freq.get("TIMESTAMP", 0),
        "count_number": freq.get("NUMBER", 0),
        "count_blockhash": freq.get("BLOCKHASH", 0),
        "count_add": freq.get("ADD", 0),
        "count_mul": freq.get("MUL", 0),
        "count_sub": freq.get("SUB", 0),
    }
    return np.array([list(features.values())]), list(features.keys())


@app.route('/api/analyze', methods=['POST'])
def analyze():
    # 1. Catch the file
    if 'file' not in request.files:
        return jsonify({"error": "No file part provided."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        raw_content = file.read().decode('utf-8').strip()
    except Exception as e:
        return jsonify({"error": f"Could not read file text: {str(e)}"}), 400

    if not raw_content:
        return jsonify({"error": "File is empty"}), 400

    # 1.5 Parse Solidity Code dynamically if it's a .sol file
    if file.filename.endswith('.sol'):
        import solcx
        import re
        version_to_install = "0.8.0"
        match = re.search(r"pragma solidity [^0-9]*([0-9]+\.[0-9]+\.[0-9]+)", raw_content)
        if match:
            version_to_install = match.group(1)
        
        try:
            solcx.install_solc(version_to_install)
            solcx.set_solc_version(version_to_install)
            compiled = solcx.compile_source(raw_content)
            
            bin_runtime = ""
            for contract_id, contract_interface in compiled.items():
                b = contract_interface.get('bin-runtime', "")
                if len(b) > len(bin_runtime):
                    bin_runtime = b
                    
            if not bin_runtime:
                return jsonify({"error": "Contracts compiled, but could not extract binary runtime."}), 400
            
            raw_content = bin_runtime
        except Exception as e:
            return jsonify({"error": f"Solidity compilation failed. External imports like @openzeppelin are currently unsupported in this demo. Details: {e}"}), 400

    # 2. Extract Opcodes exactly like Streamlit
    opcodes = bytecode_to_opcodes(raw_content)
    clean_opcodes = [op for op in opcodes if op != "UNKNOWN"]

    if len(clean_opcodes) == 0:
        return jsonify({"error": "No valid Ethereum opcodes extracted from file."}), 400

    freq = Counter(clean_opcodes)
    total = sum(freq.values())
    
    input_features, feature_names = extract_features_from_opcodes(clean_opcodes)

    # 3. Hybrid Routing Logic (Microscopic vs Macroscopic)
    if total < 50:
        confidence = 0.99
        has_time = any(op in clean_opcodes for op in ["TIMESTAMP", "NUMBER", "BLOCKHASH"])
        has_math = any(op in clean_opcodes for op in ["ADD", "MUL", "SUB"])
        has_call = "CALL" in clean_opcodes
        has_sstore = "SSTORE" in clean_opcodes
        has_ether_lock = any(op in clean_opcodes for op in ["BALANCE", "SELFDESTRUCT", "CALLVALUE", "DELEGATECALL"])

        if has_time:
            pred_class = list(label_encoder.classes_).index("block_dependency")
        elif has_ether_lock:
            pred_class = list(label_encoder.classes_).index("ether_lock")
        elif has_call and not has_sstore and not has_math:
            pred_class = list(label_encoder.classes_).index("ether_lock")
        elif has_call and has_sstore:
            pred_class = list(label_encoder.classes_).index("reentrancy")
        elif has_sstore and not has_call and not has_math:
            pred_class = list(label_encoder.classes_).index("ether_lock")
        elif has_math:
            pred_class = list(label_encoder.classes_).index("integer")
        else:
            pred_class = list(label_encoder.classes_).index("reentrancy")
            confidence = 0.50
        
        label = label_encoder.classes_[pred_class]
    else:
        # Deep Learning Path
        seq = tokenizer.texts_to_sequences([" ".join(opcodes)])
        padded = pad_sequences(seq, maxlen=MAX_LEN, padding='post', truncating='post')
        input_tensor = tf.convert_to_tensor(padded)
        
        prediction = blockguard_model(input_tensor).numpy()
        pred_class = int(np.argmax(prediction[0]))
        dl_confidence = float(prediction[0][pred_class])
        dl_label = label_encoder.classes_[pred_class]

        # ML Decision Tree Arbitration (Resolving LSTM Out-Of-Distribution Falloff)
        try:
            rf_probs = rf_model.predict_proba(input_features)[0]
            rf_pred_class = int(np.argmax(rf_probs))
            rf_label = rf_model.classes_[rf_pred_class]
            rf_confidence = float(rf_probs[rf_pred_class])
            
            # Ensembling: If RF specifically detects a high-threat semantic mismatch from DL, defer to the RF logic
            if rf_label in ["reentrancy", "integer", "block_dependency"]:
                label = rf_label
                confidence = rf_confidence
            else:
                label = dl_label
                confidence = dl_confidence
        except:
            label = dl_label
            confidence = dl_confidence

    # 4. Risk Categorization
    if confidence > 0.7:
        risk = "HIGH"
    elif confidence > 0.4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # 5. Extract SHAP Data for Front-End React Graphing
    shap_data = []
    try:
        explainer = shap.TreeExplainer(rf_model)
        shap_values = explainer.shap_values(input_features)

        if isinstance(shap_values, list):
            class_shap_values = shap_values[pred_class]
        elif len(shap_values.shape) == 3:
            class_shap_values = shap_values[:, :, pred_class]
        else:
            class_shap_values = shap_values

        for idx, feat_name in enumerate(feature_names):
            val = float(class_shap_values[0][idx])
            shap_data.append({"feature": feat_name.replace("count_", "").upper(), "impact": val})
            
    except Exception as e:
        shap_data = []

    # 6. Top Opcode Frequency for Graphing
    top_ops = freq.most_common(12)
    opcode_distribution = [{"opcode": op, "count": count} for op, count in top_ops]

    # 7. Semantic Insights
    insights = []
    if "CALL" in opcodes and "SSTORE" in opcodes:
        insights.append({"type": "risk", "msg": "Reentrancy Risk: External execution call occurs in tandem with a state update."})
    if "JUMPI" in opcodes:
        insights.append({"type": "warning", "msg": "Conditional Branching: Substantial conditional logic (JUMPI) detected."})
    if any(op in clean_opcodes for op in ["ADD", "SUB", "MUL"]):
        insights.append({"type": "warning", "msg": "Arithmetic Computation: Math operations executed natively without safe math wrappers."})
    if "TIMESTAMP" in opcodes or "NUMBER" in opcodes:
        insights.append({"type": "info", "msg": "Environment Reliance: Uses miner-manipulable environmental variables."})

    return jsonify({
        "status": "success",
        "data": {
            "prediction": {
                "vulnerability": label.replace('_', ' ').title(),
                "confidence": confidence,
                "risk": risk
            },
            "shap_data": shap_data,
            "opcode_distribution": opcode_distribution,
            "insights": insights
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
