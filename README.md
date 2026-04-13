# 🛡️ BlockGuard: Hybrid AI Vulnerability Scanner

### Next-Gen Smart Contract Security with Deep Learning, Heuristic Arbitration, and Multi-Layer XAI

---

## 🚀 Overview

**BlockGuard** is a professional-grade vulnerability detection platform for Ethereum smart contracts. Unlike traditional static analyzers, BlockGuard utilizes a **Hybrid AI Engine** that combines sequential Deep Learning (LSTM) with structural Machine Learning (Random Forest) to provide high-precision, zero-shot detection of critical security flaws.

By analyzing raw EVM bytecode directly, BlockGuard identifies:
* 🔴 **Reentrancy**: Malicious recursive call loops.
* 🟠 **Integer Overflow**: Arithmetic rollover logic flaws.
* 🟡 **Block Dependency**: Miner-manipulable entropy sources.
* 🔵 **Ether Lock**: Permanent freezing of digital assets.

---

## 🏗️ Advanced Architecture

BlockGuard operates on a modern, decoupled full-stack architecture:

1. **Frontend (React + Vite + Tailwind CSS)**: A sleek, dark-themed "Cyber-Ops" dashboard for file uploads and interactive visualization.
2. **Backend (Flask API)**: A robust Python server hosting the AI models and the dynamic Solidity compiler.
3. **Core Intelligence**:
    *   **LSTM Network**: Sequential analysis of opcode patterns (NLP-style).
    *   **Random Forest Classifier**: Structural metric evaluation for macroscopic validation.
    *   **Hybrid Arbitration**: A logical layer that resolves neural "overconfidence" by cross-referencing heuristic opcode frequencies.

---

## 🗂️ Project Structure

The repository is organized for high-fidelity auditing and research:

```
BlockGuard/
├── backend/            # Flask API Server (AI Engine)
├── frontend/           # React + Vite Dashboard
├── samples/            # Test .sol Smart Contracts
├── scripts/            # Training & Utility Scripts
├── results/            # Analytical Diagnostic Plots
├── tests/              # Internal Verification Suites
├── models/             # Serialized ML/DL model files
├── feature_engineering/# Opcode extraction logic
├── venv/               # Python Virtual Environment
└── requirements.txt    # Dependency Manifest
```

---

## 📈 Analytical Results

BlockGuard generates high-resolution diagnostic results located in the `results/` folder:
*   **Confusion Matrix**: Visualizing performance across all 4 vulnerability classes.
*   **Inference Latency**: Benchmarking BlockGuard's sub-second speed against Mythril/Slither.
*   **Feature Importance**: Mapping which opcodes (like `CALL` and `SSTORE`) influence the AI most.

---

## ⚙️ Setup & Installation

### 1️⃣ Clone and Environment
```bash
git clone https://github.com/your-username/blockguard.git
cd blockguard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Start Backend (Port 5001)
```bash
cd backend
python app.py
```

### 3️⃣ Start Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

---

## 🧠 Methodology: The Hybrid Approach

BlockGuard addresses the "Softmax Overconfidence" problem in neural networks using an **Arbitration Protocol**:
*   **Sequential Scan**: The LSTM "reads" the first 500 opcodes.
*   **Structural Scan**: The Random Forest maps the global frequency of sensitive instructions.
*   **Logical Tie-break**: If the LSTM predicts with high confidence but ignores structural indicators (like missing `SSTORE` in a balance update), the Random Forest threshold overrides the final result to ensure accuracy.

---

## ⚠️ Limitations & Future Scope
*   **External Imports**: Currently optimized for standalone `.sol` files (flattened contracts).
*   **Cloud Deployment**: Future roadmap includes AWS/Vercel integration for public API access.
*   **L2 Support**: Expanding datasets beyond Ethereum L1 to include Arbitrum and Polygon bytecode nuances.

---

## 👨‍💻 Author
**Varad Alshi**  
*BTech Computer Science | Blockchain Security Research*

---

## 📌 Final Note
BlockGuard is not just a scanner—it’s an **interpretable AI ecosystem** that bridges the gap between raw EVM execution and human-readable security audits.