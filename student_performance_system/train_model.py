# Machine learning model training script
# Predicts academic performance without attendance as an input feature

import os
import json
import numpy as np
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "student_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "performance_model.joblib")
FEATURES = ["internal_marks", "assignment_marks", "previous_marks", "study_hours"]


class AcademicLinearModel:
    """Robust, pure-numpy regression model that is immune to Windows Application Control DLL blocks."""
    def __init__(self, feature_names=None):
        self.feature_names = feature_names or FEATURES
        self.weights = None
        self.intercept = 0.0

    def fit(self, X, y):
        X_arr = np.array(X, dtype=float)
        y_arr = np.array(y, dtype=float)
        # Add bias column for intercept
        X_bias = np.c_[np.ones(len(X_arr)), X_arr]
        # Solve least squares (X_bias.T @ X_bias)^-1 @ X_bias.T @ y
        params, residuals, rank, s = np.linalg.lstsq(X_bias, y_arr, rcond=None)
        self.intercept = float(params[0])
        self.weights = [float(w) for w in params[1:]]
        return self

    def predict(self, X):
        X_arr = np.array(X, dtype=float)
        preds = self.intercept + np.dot(X_arr, self.weights)
        return np.clip(preds, 0, 100)


def create_demo_dataset(rows=1500, seed=42):
    rng = np.random.default_rng(seed)
    attendance = rng.uniform(45, 100, rows)
    internal_marks = rng.uniform(20, 100, rows)
    assignment_marks = rng.uniform(20, 100, rows)
    previous_marks = rng.uniform(25, 100, rows)
    study_hours = rng.uniform(0.5, 8, rows)

    # Attendance is kept in academic data records if needed, but excluded from prediction input features
    final_marks = (
        0.32 * internal_marks
        + 0.22 * assignment_marks
        + 0.36 * previous_marks
        + 2.0 * study_hours
        + rng.normal(0, 3.5, rows)
    )
    final_marks = np.clip(final_marks, 0, 100)

    return pd.DataFrame({
        "attendance": attendance,
        "internal_marks": internal_marks,
        "assignment_marks": assignment_marks,
        "previous_marks": previous_marks,
        "study_hours": study_hours,
        "final_marks": final_marks,
    })


def load_dataset(force_recreate=True):
    if os.path.exists(DATASET_PATH) and not force_recreate:
        return pd.read_csv(DATASET_PATH)
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    data = create_demo_dataset()
    data.to_csv(DATASET_PATH, index=False)
    print("Created synthetic demonstration dataset:", DATASET_PATH)
    return data


def train_and_save():
    data = load_dataset(force_recreate=True).dropna()
    missing_features = [f for f in FEATURES if f not in data.columns]
    if missing_features or "final_marks" not in data.columns:
        raise ValueError("Dataset must contain: " + ", ".join(FEATURES + ["final_marks"]))

    # 80/20 train/test split
    n = len(data)
    train_size = int(0.8 * n)
    indices = np.random.default_rng(42).permutation(n)
    train_idx, test_idx = indices[:train_size], indices[train_size:]

    X_train = data.iloc[train_idx][FEATURES].values
    y_train = data.iloc[train_idx]["final_marks"].values
    X_test = data.iloc[test_idx][FEATURES].values
    y_test = data.iloc[test_idx]["final_marks"].values

    model = AcademicLinearModel(feature_names=FEATURES)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = float(np.mean(np.abs(y_test - predictions)))
    rmse = float(np.sqrt(np.mean((y_test - predictions) ** 2)))
    ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
    ss_res = np.sum((y_test - predictions) ** 2)
    r2 = float(1 - (ss_res / ss_tot))

    model_payload = {
        "model_name": "Multi-Variable Linear Regression (Attendance Excluded)",
        "features": FEATURES,
        "intercept": model.intercept,
        "weights": dict(zip(FEATURES, model.weights)),
        "metrics": {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "R2": round(r2, 4)},
    }

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model_payload, MODEL_PATH)

    # Also save as json backup
    json_path = os.path.splitext(MODEL_PATH)[0] + ".json"
    with open(json_path, "w") as f:
        json.dump(model_payload, f, indent=2)

    print("Model Evaluation without Attendance:")
    print(f"MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.4f}")
    print(f"Intercept: {model.intercept:.2f}")
    for feat, w in zip(FEATURES, model.weights):
        print(f"Weight ({feat}): {w:.4f}")
    print("Saved model to:", MODEL_PATH)


if __name__ == "__main__":
    train_and_save()
