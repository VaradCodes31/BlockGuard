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
    "BLOCKHASH"
]


def build_feature_vector(bytecode):
    opcodes = bytecode_to_opcodes(bytecode)

    opcode_counts = Counter(opcodes)

    features = {}

    total_ops = len(opcodes)

    # Basic structural features
    features["total_opcodes"] = total_ops
    features["unique_opcodes"] = len(set(opcodes))

    # Important opcode counts
    for op in IMPORTANT_OPCODES:
        features[f"count_{op.lower()}"] = opcode_counts.get(op, 0)

    # Full opcode frequency features
    for op, count in opcode_counts.items():
        features[f"freq_{op.lower()}"] = count / total_ops

    return features


def process_dataset(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    feature_rows = []

    for index, row in df.iterrows():
        features = build_feature_vector(row["bytecode"])
        features["vuln_type"] = row["vuln_type"]
        feature_rows.append(features)

        if index % 500 == 0:
            print(f"Processed {index} contracts...")

    feature_df = pd.DataFrame(feature_rows)

    # Fill missing opcode columns with 0
    feature_df = feature_df.fillna(0)

    feature_df.to_csv(output_csv, index=False)

    print("\nFeature dataset saved to:", output_csv)
    print("Total features:", feature_df.shape[1])


if __name__ == "__main__":
    process_dataset(
        "../data/processed/kaggle_merged.csv",
        "../data/processed/kaggle_features_v2.csv"
    )