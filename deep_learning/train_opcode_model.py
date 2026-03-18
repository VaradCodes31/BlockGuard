import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load processed dataset
X = np.load("X.npy")
y = np.load("y.npy")

print("Dataset shape:", X.shape)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model parameters
VOCAB_SIZE = 111   # 110 + 1
MAX_LEN = 500
NUM_CLASSES = 4

# Build model
model = Sequential()

model.add(Embedding(
    input_dim=VOCAB_SIZE,
    output_dim=64,
    input_length=MAX_LEN
))

model.add(LSTM(64))

model.add(Dense(32, activation="relu"))

model.add(Dense(NUM_CLASSES, activation="softmax"))

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train model
model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test)

print("\nTest Accuracy:", accuracy)

# Save model
model.save("blockguard_opcode_model.h5")
print("Model saved successfully")