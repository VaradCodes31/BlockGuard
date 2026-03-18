import pandas as pd
import os

DATA_PATH = "../data/raw/"
OUTPUT_PATH = "../data/processed/kaggle_merged.csv"

FILES = {
    "reentrancy.csv": "reentrancy",
    "integer.csv": "integer",
    "block_dependancy.csv": "block_dependency",
    "etherlock.csv": "ether_lock"
}


def load_and_label(file_name, label):
    file_path = os.path.join(DATA_PATH, file_name)
    
    print(f"Loading {file_name}...")
    df = pd.read_csv(file_path)

    # Print columns to verify structure
    print("Columns found:", df.columns.tolist())

    # Keep only required columns
    df = df[["contract_address", "bytecode"]].copy()

    # Add vulnerability type
    df["vuln_type"] = label

    print(f"Loaded {len(df)} samples.\n")
    return df


def main():
    all_dfs = []

    for file, label in FILES.items():
        df = load_and_label(file, label)
        all_dfs.append(df)

    # Merge all CSVs
    merged_df = pd.concat(all_dfs, ignore_index=True)

    print("Total samples after merge:", len(merged_df))

    # Remove duplicates based on contract address
    merged_df = merged_df.drop_duplicates(subset=["contract_address"])

    print("Total samples after removing duplicates:", len(merged_df))

    # Remove rows with missing bytecode
    merged_df = merged_df.dropna(subset=["bytecode"])

    print("Total samples after removing missing bytecode:", len(merged_df))

    # Ensure processed folder exists
    os.makedirs("../data/processed", exist_ok=True)

    # Save merged dataset
    merged_df.to_csv(OUTPUT_PATH, index=False)

    print("\nMerged dataset saved successfully at:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()