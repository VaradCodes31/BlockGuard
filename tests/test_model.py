import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle

try:
    y = np.load('deep_learning/y.npy')
    print("Class distribution in y.npy:", np.unique(y, return_counts=True))

    with open('deep_learning/label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)
    print("Classes:", le.classes_)

    model = load_model('deep_learning/blockguard_opcode_model.h5')
    X = np.load('deep_learning/X.npy')

    pred = model.predict(X[:100])
    pred_classes = np.argmax(pred, axis=1)
    print("Unique predictions on first 100 samples:", np.unique(pred_classes, return_counts=True))
except Exception as e:
    print("Error:", e)
