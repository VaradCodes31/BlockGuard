import pandas as pd

df = pd.read_csv("../data/processed/combined_features.csv")

print("Original dataset size:", df.shape)

# Map SmartBugs labels to Kaggle labels
mapping = {
    "arithmetic": "integer",
    "time_manipulation": "block_dependency",
    "denial_of_service": "ether_lock"
}

df["vuln_type"] = df["vuln_type"].replace(mapping)

# Keep only the 4 target classes
valid_classes = [
    "reentrancy",
    "ether_lock",
    "integer",
    "block_dependency"
]

df = df[df["vuln_type"].isin(valid_classes)]

# Reset index
df = df.reset_index(drop=True)

df.to_csv("../data/processed/final_features.csv", index=False)

print("\nCleaned dataset shape:", df.shape)

print("\nFinal class distribution:")
print(df["vuln_type"].value_counts())