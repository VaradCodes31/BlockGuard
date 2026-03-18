import sys
import os
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Add feature_engineering folder to path
sys.path.append(os.path.abspath("../feature_engineering"))

from opcode_extractor import bytecode_to_opcodes


# Load trained model
model = load_model("blockguard_opcode_model.h5")

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load label encoder
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)


MAX_LEN = 500


def predict(bytecode):

    # Convert bytecode → opcodes
    opcodes = bytecode_to_opcodes(bytecode)

    if len(opcodes) == 0:
        print("No opcodes extracted.")
        return

    sequence = " ".join(opcodes)

    # Tokenize
    seq = tokenizer.texts_to_sequences([sequence])

    # Pad
    seq = pad_sequences(seq, maxlen=MAX_LEN, padding="post")

    # Predict
    prediction = model.predict(seq)

    class_index = np.argmax(prediction)

    vulnerability = label_encoder.inverse_transform([class_index])[0]

    confidence = prediction[0][class_index]

    print("\nBlockGuard Analysis Result")
    print("---------------------------")
    print("Predicted Vulnerability:", vulnerability)
    print("Confidence:", round(float(confidence), 4))


# Example test
if __name__ == "__main__":

    bytecode = input("Enter smart contract bytecode:\n")

    predict(bytecode)