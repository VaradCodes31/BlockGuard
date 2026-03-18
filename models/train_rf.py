import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load improved feature dataset
df = pd.read_csv("../data/processed/final_features.csv")

# Separate features and labels
X = df.drop("vuln_type", axis=1)
y = df["vuln_type"]

# Train-test split (stratified because of imbalance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

print("Training model...")
model.fit(X_train, y_train)

print("\nEvaluating model...")
y_pred = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
joblib.dump(model, "../data/processed/rf_model_v2.pkl")
print("\nModel saved successfully.")