import numpy as np
import pickle
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from tensorflow.keras.models import load_model

# -------------------------------
# Load Data
# -------------------------------
X = np.load("X.npy")
y = np.load("y.npy")

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# -------------------------------
# Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# MODEL 1: Random Forest
# -------------------------------
print("\nTraining Random Forest...")
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

print("\nRandom Forest Accuracy:", rf_acc)
print("\nRandom Forest Report:\n", classification_report(y_test, rf_pred))

# -------------------------------
# MODEL 2: SVM
# -------------------------------
print("\nTraining SVM...")
svm = SVC()
svm.fit(X_train, y_train)

svm_pred = svm.predict(X_test)
svm_acc = accuracy_score(y_test, svm_pred)

print("\nSVM Accuracy:", svm_acc)
print("\nSVM Report:\n", classification_report(y_test, svm_pred))

# -------------------------------
# MODEL 3: LSTM (Your Model)
# -------------------------------
print("\nEvaluating LSTM...")
model = load_model("blockguard_opcode_model.h5")

loss, lstm_acc = model.evaluate(X_test, y_test)

print("\nLSTM Accuracy:", lstm_acc)

# -------------------------------
# FINAL COMPARISON
# -------------------------------
print("\nFinal Model Comparison")
print("-----------------------")
print("Random Forest:", rf_acc)
print("SVM:", svm_acc)
print("LSTM:", lstm_acc)

# -------------------------------
# CONFUSION MATRIX (LSTM)
# -------------------------------
print("\nGenerating Confusion Matrix...")

lstm_pred = model.predict(X_test)
lstm_pred_classes = np.argmax(lstm_pred, axis=1)

cm = confusion_matrix(y_test, lstm_pred_classes)

plt.figure()
plt.imshow(cm)
plt.title("LSTM Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()
plt.show()

# -------------------------------
# ACCURACY BAR GRAPH
# -------------------------------
models = ["Random Forest", "SVM", "LSTM"]
accuracies = [rf_acc, svm_acc, lstm_acc]

plt.figure()
plt.bar(models, accuracies)
plt.title("Model Accuracy Comparison")
plt.xlabel("Models")
plt.ylabel("Accuracy")
plt.show()