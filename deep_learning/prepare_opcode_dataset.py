import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load dataset
df = pd.read_csv("../data/processed/opcode_sequences.csv")

print("Dataset shape:", df.shape)

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["vuln_type"])

print("\nClasses:", label_encoder.classes_)

# Tokenize opcode sequences
tokenizer = Tokenizer(filters='', lower=False, split=' ')
tokenizer.fit_on_texts(df["opcode_sequence"])

X = tokenizer.texts_to_sequences(df["opcode_sequence"])

print("\nVocabulary size:", len(tokenizer.word_index))

# Pad sequences
MAX_LEN = 500

X = pad_sequences(X, maxlen=MAX_LEN, padding="post")

print("Processed dataset shape:", X.shape)

# Save processed data
np.save("X.npy", X)
np.save("y.npy", y)

# Save tokenizer and label encoder
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("\nSaved processed dataset files")