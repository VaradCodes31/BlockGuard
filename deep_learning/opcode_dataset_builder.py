import sys
import os
import pandas as pd

sys.path.append(os.path.abspath("../feature_engineering"))

from opcode_extractor import bytecode_to_opcodes

# Load original bytecode dataset
bytecode_df = pd.read_csv("../data/processed/kaggle_merged.csv")

records = []

for i, row in bytecode_df.iterrows():

    bytecode = row["bytecode"]

    # Skip empty bytecode just in case
    if pd.isna(bytecode):
        continue

    opcodes = bytecode_to_opcodes(bytecode)

    if len(opcodes) == 0:
        continue

    sequence = " ".join(opcodes)

    records.append({
        "opcode_sequence": sequence,
        "vuln_type": row["vuln_type"]
    })

    if i % 500 == 0:
        print(f"Processed {i} contracts")

dataset = pd.DataFrame(records)

dataset.to_csv("../data/processed/opcode_sequences.csv", index=False)

print("\nSaved opcode sequence dataset:", dataset.shape)