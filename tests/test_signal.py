import numpy as np
import pickle
from tensorflow.keras.models import load_model

model = load_model('deep_learning/blockguard_opcode_model.h5')
with open('deep_learning/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)
with open('deep_learning/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

# Integer overflow typically has ADD, SUB, MUL without checking
seq1 = tokenizer.texts_to_sequences(["PUSH1 PUSH1 ADD MUL SSTORE"])
padded1 = np.zeros(500)
padded1[:len(seq1[0])] = seq1[0]
pred1 = model.predict(np.array([padded1]), verbose=0)[0]
c1 = np.argmax(pred1)
print("Integer Overflow Signal:", le.classes_[c1], "Conf:", pred1[c1])

# Ether lock typically has CALL, VALUE, BALANCE without selfdestruct
seq2 = tokenizer.texts_to_sequences(["CALL VALUE BALANCE PUSH1 SSTORE"])
padded2 = np.zeros(500)
padded2[:len(seq2[0])] = seq2[0]
pred2 = model.predict(np.array([padded2]), verbose=0)[0]
c2 = np.argmax(pred2)
print("Ether Lock Signal:", le.classes_[c2], "Conf:", pred2[c2])

# Block Dependency typically has TIMESTAMP, NUMBER, BLOCKHASH
seq3 = tokenizer.texts_to_sequences(["TIMESTAMP NUMBER BLOCKHASH PUSH1 SSTORE"])
padded3 = np.zeros(500)
padded3[:len(seq3[0])] = seq3[0]
pred3 = model.predict(np.array([padded3]), verbose=0)[0]
c3 = np.argmax(pred3)
print("Block Dependency Signal:", le.classes_[c3], "Conf:", pred3[c3])

# Empty/Random
seq4 = tokenizer.texts_to_sequences(["PUSH1 PUSH1 JUMP"])
padded4 = np.zeros(500)
padded4[:len(seq4[0])] = seq4[0]
pred4 = model.predict(np.array([padded4]), verbose=0)[0]
c4 = np.argmax(pred4)
print("Generic JUMP:", le.classes_[c4], "Conf:", pred4[c4])
