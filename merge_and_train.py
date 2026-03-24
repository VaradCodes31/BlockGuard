import pandas as pd
import os

print("Merging datasets...")
df1 = pd.read_csv("data/processed/kaggle_features_v2.csv")
df2 = pd.read_csv("data/processed/smartbugs_features.csv")
print(f"Kaggle cols: {len(df1.columns)}, Smartbugs cols: {len(df2.columns)}")

final = pd.concat([df1, df2], ignore_index=True)
final.to_csv("data/processed/final_features.csv", index=False)
print(f"Final features saved! Shape: {final.shape}")

print("\n--- Running RF Retraining ---")
os.system("./venv/bin/python retrain_rf_balanced.py")
