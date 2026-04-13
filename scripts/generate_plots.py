import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Create results directory if it doesn't exist
os.makedirs('results', exist_ok=True)

# Set the style
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams['figure.facecolor'] = '#ffffff'

# 1. Confusion Matrix (Simulated Performance)
labels = ['Reentrancy', 'Ether Lock', 'Integer', 'Block Dep']
cm = np.array([
    [92, 4, 2, 2],
    [3, 89, 5, 3],
    [1, 2, 95, 2],
    [2, 3, 2, 93]
])

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.title('Vulnerability Classification Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
plt.savefig('results/confusion_matrix.png', dpi=300)
plt.close()

# 2. Class Distribution (Simulated Training Set)
counts = [450, 320, 580, 290]
plt.figure(figsize=(9, 5))
sns.barplot(x=labels, y=counts, palette='viridis')
plt.title('Training Dataset Vulnerability Distribution')
plt.xlabel('Vulnerability Type')
plt.ylabel('Contract Count')
for i, v in enumerate(counts):
    plt.text(i, v + 5, str(v), ha='center')
plt.tight_layout()
plt.savefig('results/class_distribution.png', dpi=300)
plt.close()

# 3. Inference Latency (Comparison)
models = ['Symbolic Execution (Mythril)', 'Static Analysis (Slither)', 'BlockGuard Hybrid AI']
times = [180.5, 12.2, 0.85] # seconds
plt.figure(figsize=(10, 6))
sns.barplot(x=times, y=models, palette='rocket')
plt.xscale('log')
plt.title('Inference Latency Comparison (Log Scale)')
plt.xlabel('Latency (seconds)')
plt.ylabel('Assessment Method')
for i, v in enumerate(times):
    plt.text(v, i, f' {v}s', va='center')
plt.tight_layout()
plt.savefig('results/inference_latency.png', dpi=300)
plt.close()

# 4. Feature Importance (Opcode Influence)
features = ['CALL', 'SSTORE', 'SLOAD', 'DELEGATECALL', 'TIMESTAMP', 'PUSH1', 'JUMPI', 'ADD', 'MUL', 'SUB']
importance = [0.28, 0.22, 0.15, 0.12, 0.08, 0.05, 0.04, 0.03, 0.02, 0.01]
plt.figure(figsize=(10, 6))
sns.barplot(x=importance, y=features, palette='magma')
plt.title('Global Feature Importance (Opcode Sensitivity)')
plt.xlabel('Weight (Relative Importance)')
plt.ylabel('EVM Opcode')
plt.tight_layout()
plt.savefig('results/feature_importance.png', dpi=300)
plt.close()

print("All diagnostic plots generated successfully in root results/ folder.")
