import pickle

with open('deep_learning/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

print("Tokenizer lower:", tokenizer.lower)
print("Word index keys (first 10):", list(tokenizer.word_index.keys())[:10])

test_seq = ["PUSH1 MSTORE DUP1 REVERT"]
print("Uppercase text to seq:", tokenizer.texts_to_sequences(test_seq))
print("Lowercase text to seq:", tokenizer.texts_to_sequences([s.lower() for s in test_seq]))
