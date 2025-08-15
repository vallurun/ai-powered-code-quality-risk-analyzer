import json, os, joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model.joblib")

def train_demo():
    # Synthetic training data: [num_files, lines_added, lines_removed, num_py_files, avg_cc]
    X = np.array([
        [1, 10, 2, 1, 1.2],
        [5, 400, 300, 2, 3.5],
        [2, 50, 10, 0, 0.5],
        [3, 200, 20, 1, 2.1],
        [6, 800, 700, 3, 4.2],
        [1, 5, 1, 0, 0.2],
    ], dtype=float)
    y = np.array([0, 1, 0, 1, 1, 0], dtype=int)
    m = LogisticRegression().fit(X, y)
    joblib.dump(m, MODEL_PATH)
    return MODEL_PATH

def load_model():
    import joblib
    if not os.path.exists(MODEL_PATH):
        train_demo()
    return joblib.load(MODEL_PATH)

if __name__ == "__main__":
    p = train_demo()
    print("Model saved to", p)
