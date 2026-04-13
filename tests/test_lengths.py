import numpy as np

X = np.load('deep_learning/X.npy')
y = np.load('deep_learning/y.npy')

for c in range(4):
    X_c = X[y == c]
    # count non-zero tokens per sequence
    lengths = np.sum(X_c != 0, axis=1)
    print(f"Class {c}: mean length = {np.mean(lengths):.1f}, median = {np.median(lengths):.1f}, min = {np.min(lengths)}, max = {np.max(lengths)}")

# Check predictions based on sequence length
try:
    from tensorflow.keras.models import load_model
    model = load_model('deep_learning/blockguard_opcode_model.h5')
    
    # Create artificial sequences of varying lengths (e.g. just PUSH1 tokens = 1)
    for length in [10, 50, 100, 200, 400, 500]:
        seq = np.zeros(500)
        seq[:length] = 1 # Token 1 is PUSH1
        pred = model.predict(np.array([seq]), verbose=0)
        print(f"Length {length} prediction: {np.argmax(pred)} with confidence {np.max(pred):.2f}")
except Exception as e:
    print("Error:", e)
