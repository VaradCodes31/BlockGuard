import pandas as pd
from collections import Counter
from opcode_extractor import bytecode_to_opcodes

IMPORTANT_OPCODES = [
    "CALL",
    "DELEGATECALL",
    "STATICCALL",
    "CALLCODE",
    "SSTORE",
    "SLOAD",
    "JUMP",
    "JUMPI",
    "SELFDESTRUCT",
    "REVERT",
    "TIMESTAMP",
    "NUMBER",
    "BLOCKHASH",
    "ADD",
    "MUL",
    "SUB"
]


def build_feature_vector(bytecode):

    opcodes = bytecode_to_opcodes(bytecode)

    opcode_counts = Counter(opcodes)

    features = {}

    total_ops = len(opcodes)

    features["total_opcodes"] = total_ops
    features["unique_opcodes"] = len(set(opcodes))

    for op in IMPORTANT_OPCODES:
        features[f"count_{op.lower()}"] = opcode_counts.get(op, 0)

    return features


def process_dataset(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    feature_rows = []

    for index, row in df.iterrows():

        features = build_feature_vector(row["bytecode"])

        features["vuln_type"] = row["vuln_type"]

        feature_rows.append(features)

        if index % 10 == 0:
            print(f"Processed {index} contracts")

    feature_df = pd.DataFrame(feature_rows)

    feature_df = feature_df.fillna(0)

    feature_df.to_csv(output_csv, index=False)

    print("\nSaved SmartBugs features:", feature_df.shape)


if __name__ == "__main__":

    process_dataset(
        "../data/processed/smartbugs_bytecode.csv",
        "../data/processed/smartbugs_features.csv"
    )