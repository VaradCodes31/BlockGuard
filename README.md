# 🛡️ BlockGuard

### AI-Powered Smart Contract Vulnerability Detection with Explainable AI (XAI)

---

## 🚀 Overview

**BlockGuard** is an AI-based system designed to detect vulnerabilities in Ethereum smart contracts using **Deep Learning + Explainable AI (XAI)**.

It analyzes smart contract bytecode, converts it into opcode sequences, and predicts potential vulnerabilities such as:

* 🔴 Reentrancy
* 🟠 Integer Overflow
* 🟡 Block Dependency
* 🔵 Ether Lock

Along with predictions, BlockGuard provides **interpretable insights** using a hybrid explainability approach.

---

## 🧠 Key Features

### 🔍 1. Vulnerability Detection

* LSTM-based deep learning model
* Multi-class classification of smart contract vulnerabilities
* High accuracy (~83%)

---

### 📊 2. Hybrid Explainability (XAI)

BlockGuard uses a **multi-layer XAI system**:

* ✅ Gradient-based opcode importance
* ✅ Opcode frequency analysis
* ✅ Rule-based vulnerability insights
* ✅ Visual heatmap representation

---

### 🔥 3. Opcode Heatmap Visualization

Visual representation of opcode importance:

```
PUSH1      ██████████
DUP3       ███
EQ         ██
```

Helps identify critical execution patterns.

---

### 🧠 4. Derived Insights

Human-readable explanations like:

* Conditional logic detected
* External calls present
* Heavy stack usage
* Potential reentrancy patterns

---

### 🌐 5. Interactive Dashboard (Streamlit)

* Paste bytecode
* Get prediction instantly
* View heatmap + insights
* Risk level visualization

---

## 🏗️ Project Architecture

```
Bytecode Input
      ↓
Opcode Extraction
      ↓
Tokenization & Padding
      ↓
LSTM Model
      ↓
Prediction
      ↓
Explainability Layer
   ├── Gradient Signals
   ├── Frequency Analysis
   ├── Rule-based Insights
   └── Heatmap Visualization
```

---

## 🗂️ Project Structure

```
BlockGuard/
│
├── deep_learning/
│   ├── train_opcode_model.py
│   ├── explain_prediction.py
│
├── feature_engineering/
│   └── opcode_extractor.py
│
├── dashboard/
│   └── app.py
│
├── data/
│
├── tokenizer.pkl
├── label_encoder.pkl
├── blockguard_opcode_model.h5
│
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/blockguard.git
cd blockguard
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install tensorflow pandas numpy scikit-learn streamlit
```

---

## ▶️ Usage

---

### 🔹 Run CLI Version

```bash
cd deep_learning
python explain_prediction.py
```

Enter bytecode when prompted.

---

### 🔹 Run Web Dashboard

```bash
cd dashboard
python -m streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 📈 Example Output

```
BlockGuard Prediction
---------------------
Vulnerability: reentrancy
Confidence: 0.7733

Opcode Heatmap
----------------
PUSH1      ██████████
DUP3       ███
EQ         ██

Derived Insights
-----------------
• Conditional logic present
• Heavy stack usage detected

Risk Level: HIGH
```

---

## 🧪 Tech Stack

* **Python**
* **TensorFlow / Keras**
* **NumPy / Pandas**
* **Streamlit**
* **Scikit-learn**

---

## 🧠 Methodology

1. Bytecode → Opcode conversion
2. Tokenization & padding
3. LSTM-based sequence modeling
4. Multi-class vulnerability classification
5. Explainability using:

   * Gradient-based attribution
   * Frequency analysis
   * Rule-based logic

---

## 🔬 Novelty

BlockGuard introduces a **hybrid XAI approach**:

* Combines deep learning with interpretable outputs
* Uses **opcode-level analysis instead of source code**
* Provides **visual + textual explanations**
* Bridges gap between **AI predictions and developer understanding**

---

## ⚠️ Limitations

* Gradient-based explanations are weak due to LSTM compression
* Works only on bytecode-level (not Solidity source directly)
* Requires further validation on large real-world datasets

---

## 🚀 Future Improvements

* 🔥 Attention-based models (Transformer)
* 🎨 Advanced heatmap visualization
* 📁 Upload Solidity (.sol) files
* 🌐 Deploy as web service
* 🔐 Integrate with blockchain security tools

---

## 👨‍💻 Author

**Varad Alshi**
BTech Computer Science

---

## ⭐ Acknowledgements

* Ethereum opcode documentation
* Kaggle smart contract datasets
* TensorFlow & Streamlit communities

---

## 📌 Final Note

BlockGuard is not just a prediction model —
it’s an **interpretable AI system for blockchain security**.