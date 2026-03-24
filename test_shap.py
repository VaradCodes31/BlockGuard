import numpy as np
import shap
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

X = np.random.rand(10, 15)
y = np.random.randint(0, 4, 10)
rf = RandomForestClassifier()
rf.fit(X, y)

explainer = shap.TreeExplainer(rf)
shap_res = explainer.shap_values(X[0:1])

fig, ax = plt.subplots()
try:
    # Get importance for class 0
    if len(shap_res.shape) == 3:
        class_shap = shap_res[:, :, 0]
    elif isinstance(shap_res, list):
        class_shap = shap_res[0]
        
    shap.summary_plot(class_shap, X[0:1], feature_names=[f"F{i}" for i in range(15)], show=False, plot_type="bar")
    plt.savefig("test_plot_bar.png")
    print("Plot bar saved successfully.")
except Exception as e:
    print("Error:", e)
