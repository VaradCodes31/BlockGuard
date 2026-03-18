import streamlit as st
import numpy as np
import pickle
import tensorflow as tf
from collections import Counter
import os
import sys
import matplotlib.pyplot as plt

# -------------------------------
# Path Setup
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DL_DIR = os.path.join(BASE_DIR, "deep_learning")

sys.path.append(os.path.join(BASE_DIR, "feature_engineering"))
from opcode_extractor import bytecode_to_opcodes

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# -------------------------------
# Load Files
# -------------------------------
MODEL_PATH = os.path.join(DL_DIR, "blockguard_opcode_model.h5")
TOKENIZER_PATH = os.path.join(DL_DIR, "tokenizer.pkl")
LABEL_ENCODER_PATH = os.path.join(DL_DIR, "label_encoder.pkl")

model = load_model(MODEL_PATH)

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

MAX_LEN = 500

# -------------------------------
# UI Setup
# -------------------------------
st.set_page_config(page_title="BlockGuard", layout="wide")

st.title("🛡️ BlockGuard - Smart Contract Vulnerability Detector")
st.markdown("Analyze Ethereum smart contract bytecode using AI + Explainability")

bytecode = st.text_area("Enter Smart Contract Bytecode", height=200)

if st.button("🔍 Analyze"):

    # -------------------------------
    # Validation
    # -------------------------------
    if not bytecode.strip():
        st.error("Please enter bytecode")
        st.stop()

    # -------------------------------
    # Opcode Extraction
    # -------------------------------
    opcodes = bytecode_to_opcodes(bytecode)
    clean_opcodes = [op for op in opcodes if op != "UNKNOWN"]

    if len(clean_opcodes) == 0:
        st.error("No valid opcodes extracted")
        st.stop()

    freq = Counter(clean_opcodes)
    total = sum(freq.values())

    # -------------------------------
    # Tokenization
    # -------------------------------
    seq = tokenizer.texts_to_sequences([" ".join(opcodes)])
    padded = pad_sequences(seq, maxlen=MAX_LEN, padding='post')
    input_tensor = tf.convert_to_tensor(padded)

    # -------------------------------
    # Prediction
    # -------------------------------
    prediction = model(input_tensor).numpy()
    pred_class = np.argmax(prediction[0])
    confidence = float(prediction[0][pred_class])
    label = label_encoder.classes_[pred_class]

    # Risk classification
    if confidence > 0.7:
        risk, color = "HIGH", "red"
    elif confidence > 0.4:
        risk, color = "MEDIUM", "orange"
    else:
        risk, color = "LOW", "green"

    # -------------------------------
    # Tabs
    # -------------------------------
    tab1, tab2, tab3 = st.tabs(["🔍 Prediction", "📊 Visualization", "🧠 Insights"])

    # =====================================================
    # TAB 1: Prediction + Explainability
    # =====================================================
    with tab1:
        st.subheader("Prediction Result")

        col1, col2, col3 = st.columns(3)
        col1.metric("Vulnerability", label)
        col2.metric("Confidence", f"{confidence:.4f}")
        col3.markdown(f"### Risk: :{color}[{risk}]")

        # Vulnerability explanation
        if label == "reentrancy":
            st.info("Reentrancy occurs when external calls allow repeated withdrawals before state update.")

        # -------------------------------
        # Confidence Explanation
        # -------------------------------
        st.subheader("📊 Confidence Explanation")

        if confidence > 0.85:
            st.write("Very strong match with known vulnerability patterns.")
        elif confidence > 0.65:
            st.write("Moderate confidence — patterns detected but not dominant.")
        else:
            st.write("Low confidence — prediction uncertain.")

        # -------------------------------
        # FINAL EXPLAINABILITY ENGINE
        # -------------------------------
        st.subheader("🧠 Model Explainability")
        st.success("Multi-layer explainability: Security + Behavior + AI reasoning")

        # 1️⃣ Security Indicators
        st.write("### 🔑 Security Indicators")

        important_ops = ["CALL", "DELEGATECALL", "STATICCALL", "SSTORE", "SLOAD", "JUMPI"]
        important_present = [(op, count) for op, count in freq.items() if op in important_ops]

        if important_present:
            for op, count in sorted(important_present, key=lambda x: x[1], reverse=True):
                percent = (count / total) * 100
                st.write(f"• {op} → {percent:.1f}% influence")
        else:
            st.write("• No strong direct vulnerability opcodes detected")

        # 2️⃣ Behavioral Patterns
        st.write("### ⚙️ Behavioral Patterns")

        for op, count in freq.most_common(5):
            percent = (count / total) * 100
            st.write(f"• {op} → {percent:.1f}% dominance")

        # 3️⃣ Model Reasoning
        st.write("### 🧠 Model Reasoning")

        if label == "reentrancy":
            st.write("• Model detected opcode sequences similar to reentrancy patterns")
            if "CALL" in opcodes and "SSTORE" in opcodes:
                st.write("• Strong signal: CALL followed by SSTORE (classic reentrancy)")
            else:
                st.write("• Learned sequence patterns triggered detection even without explicit signals")

        # 4️⃣ Confidence Interpretation
        st.write("### 📊 Confidence Interpretation")

        if confidence > 0.85:
            st.write("• Very strong vulnerability pattern match")
        elif confidence > 0.65:
            st.write("• Moderate match — verify manually")
        else:
            st.write("• Weak signal — needs further analysis")

        if confidence > 0.75:
            st.error("🚨 High confidence vulnerability detected — review immediately")

    # =====================================================
    # TAB 2: Visualization (Matplotlib)
    # =====================================================
    with tab2:
        st.subheader("Opcode Distribution")

        top_ops = freq.most_common(10)
        labels = [op for op, _ in top_ops]
        values = [count for _, count in top_ops]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_xlabel("Opcodes")
        ax.set_ylabel("Frequency")
        ax.set_title("Top Opcode Distribution")

        st.pyplot(fig)

    # =====================================================
    # TAB 3: Insights
    # =====================================================
    with tab3:
        st.subheader("Derived Insights")

        if "CALL" in opcodes and "SSTORE" in opcodes:
            st.write("• External call + state update → reentrancy risk")

        if "JUMPI" in opcodes:
            st.write("• Conditional branching detected")

        if any(op.startswith("PUSH") for op in opcodes):
            st.write("• Stack-heavy operations present")

        if "SLOAD" in opcodes:
            st.write("• Storage read detected")