import pandas as pd

# Load datasets
kaggle_df = pd.read_csv("../data/processed/kaggle_features_v2.csv")
smartbugs_df = pd.read_csv("../data/processed/smartbugs_features.csv")

print("Kaggle dataset:", kaggle_df.shape)
print("SmartBugs dataset:", smartbugs_df.shape)

# Combine datasets
combined_df = pd.concat([kaggle_df, smartbugs_df], ignore_index=True)

# Fill missing feature columns
combined_df = combined_df.fillna(0)

# Save merged dataset
combined_df.to_csv("../data/processed/combined_features.csv", index=False)

print("\nCombined dataset saved.")
print("Final shape:", combined_df.shape)

print("\nClass distribution:")
print(combined_df["vuln_type"].value_counts())