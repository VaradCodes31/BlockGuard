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

# ======= DATA AUGMENTATION (Hybrid Approach) =======
print("Original X_train shape:", X_train.shape)
X_resampled = []
y_resampled = []

target_sizes = {
    0: 500,   # Oversample from 110 (prevent massive overfitting)
    1: 1365,  # Keep as is
    2: 1000,  # Slight oversample from 927
    3: 1365   # Undersample from 5431
}

for c in np.unique(y_train):
    X_c = X_train[y_train == c]
    if len(X_c) > 0:
        target_size = target_sizes.get(c, len(X_c))
        if target_size > len(X_c):
            # Oversample
            indices = np.random.choice(len(X_c), target_size, replace=True)
            X_resampled.append(X_c[indices])
        else:
            # Undersample or Keep
            indices = np.random.choice(len(X_c), target_size, replace=False)
            X_resampled.append(X_c[indices])
        y_resampled.append(np.full(target_size, c))

X_train_res = np.vstack(X_resampled)
y_train_res = np.concatenate(y_resampled)

# Model parameters
VOCAB_SIZE = 111   # 110 + 1
MAX_LEN = 500
NUM_CLASSES = 4

X_train = X_train_res
y_train = y_train_res

# Shuffle the final augmented dataset
shuffle_idx = np.random.permutation(len(X_train))
X_train = X_train[shuffle_idx]
y_train = y_train[shuffle_idx]
print("Final Balanced X_train shape:", X_train.shape)
# =======================================================

# Build model
from tensorflow.keras.layers import Dropout, GlobalAveragePooling1D

model = Sequential()

model.add(Embedding(
    input_dim=VOCAB_SIZE,
    output_dim=64,
    input_length=MAX_LEN,
    mask_zero=True
))

model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=True, recurrent_dropout=0.2))
model.add(GlobalAveragePooling1D())

model.add(Dense(32, activation="relu"))
model.add(Dropout(0.2))

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