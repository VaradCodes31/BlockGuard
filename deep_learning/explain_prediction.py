import sys
import os
import numpy as np
import pickle
import tensorflow as tf
from collections import Counter

# Add feature_engineering path
sys.path.append(os.path.abspath("../feature_engineering"))
from opcode_extractor import bytecode_to_opcodes

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# -------------------------------
# Load Model & Tokenizer
# -------------------------------
model = load_model("blockguard_opcode_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

MAX_LEN = 500  # MUST match training

# -------------------------------
# Input Bytecode
# -------------------------------
bytecode = input("Enter smart contract bytecode:\n")

# -------------------------------
# Convert Bytecode → Opcodes
# -------------------------------
opcodes = bytecode_to_opcodes(bytecode)

if len(opcodes) == 0:
    print("Error: Could not extract opcodes.")
    sys.exit()

# -------------------------------
# Tokenization
# -------------------------------
sequence = tokenizer.texts_to_sequences([" ".join(opcodes)])
padded = pad_sequences(sequence, maxlen=MAX_LEN, padding='post')

input_tensor = tf.convert_to_tensor(padded)

# -------------------------------
# Gradient-based Explainability
# -------------------------------
embedding_layer = model.layers[0]

with tf.GradientTape() as tape:

    embedded = embedding_layer(input_tensor)
    tape.watch(embedded)

    x = embedded
    for layer in model.layers[1:]:
        x = layer(x)

    prediction = x

    class_idx = int(tf.argmax(prediction[0]))
    loss = prediction[:, class_idx]

# Compute gradients
grads = tape.gradient(loss, embedded)

if grads is None:
    print("Error: Gradients could not be computed.")
    sys.exit()

# -------------------------------
# Importance Calculation
# -------------------------------
importance = tf.reduce_sum(tf.abs(grads), axis=2).numpy()[0]

# Normalize safely
max_val = np.max(importance)
if max_val > 0:
    importance = importance / max_val

# -------------------------------
# Map Importance to Opcodes
# -------------------------------
opcode_importance = []

for i in range(min(len(opcodes), MAX_LEN)):
    opcode_importance.append((opcodes[i], importance[i]))

# -------------------------------
# Prediction Handling
# -------------------------------
pred = prediction.numpy()

pred_class = np.argmax(pred[0])
confidence = float(pred[0][pred_class])
labels = label_encoder.classes_

# -------------------------------
# Display Prediction
# -------------------------------
print("\nBlockGuard Prediction")
print("---------------------")
print(f"Vulnerability: {labels[pred_class]}")
print(f"Confidence: {confidence:.4f}")

print("\nOpcode Heatmap (Frequency-based)")
print("----------------------------------")
print("Showing first 50 opcodes...\n")

# Get frequency
freq = Counter(opcodes)

# Normalize frequency
max_freq = max(freq.values())

for opcode in opcodes[:50]:

    score = freq[opcode] / max_freq  # 0–1 scale

    bars = int(score * 10)
    bar = "█" * bars

    print(f"{opcode:<10} | {bar:<10} | {round(score,2)}")

# -------------------------------
# Top Important Opcodes
# -------------------------------
sorted_ops = sorted(opcode_importance, key=lambda x: x[1], reverse=True)

print("\nTop Opcode Signals (Gradient-based)")
print("-----------------------------------")

top_unique = []
seen = set()

for op, score in sorted_ops:
    if op not in seen:
        top_unique.append(op)
        seen.add(op)
    if len(top_unique) == 5:
        break

for op in top_unique:
    print(op)

# -------------------------------
# Frequency Analysis
# -------------------------------
print("\nMost Frequent Opcodes")
print("----------------------")

freq = Counter(opcodes)

for op, count in freq.most_common(10):
    print(f"{op} : {count}")

# -------------------------------
# Derived Insights
# -------------------------------
print("\nDerived Insights")
print("-----------------")

if any(op in opcodes for op in ["JUMPI", "JUMP"]):
    print("• Conditional logic present")

if any(op in opcodes for op in ["CALL", "DELEGATECALL"]):
    print("• External call detected")

if any(op.startswith("DUP") or op.startswith("PUSH") for op in opcodes):
    print("• Heavy stack usage detected")

if any(op in opcodes for op in ["SSTORE", "SLOAD"]):
    print("• Storage operations detected")

if "CALL" in opcodes and "SSTORE" in opcodes:
    print("• ⚠ Potential Reentrancy Pattern")

# -------------------------------
# Risk Level
# -------------------------------
if confidence > 0.7:
    risk = "HIGH"
elif confidence > 0.4:
    risk = "MEDIUM"
else:
    risk = "LOW"

print("\nRisk Level:", risk)