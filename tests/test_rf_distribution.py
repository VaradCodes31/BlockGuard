import pandas as pd
df = pd.read_csv("data/processed/final_features.csv")
print(df.groupby('vuln_type').mean().T)
