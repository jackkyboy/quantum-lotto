# src/ml/model_pipeline.py

# src/ml/model_pipeline.py

import warnings
import joblib
import optuna
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import xgboost as xgb

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.exceptions import UndefinedMetricWarning

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

VERBOSE = True


def feature_engineering(df):
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.weekday

    digits = df["3digits"].astype(str).str.zfill(3)
    for i in range(3):
        df[f"d{i+1}"] = digits.str[i].astype(int)

    df["sum_digits"] = df[["d1", "d2", "d3"]].sum(axis=1)
    df["has_double"] = (
        (digits.str[0] == digits.str[1]) |
        (digits.str[1] == digits.str[2]) |
        (digits.str[0] == digits.str[2])
    ).astype(int)

    df["diff_1_2"] = abs(df["d1"] - df["d2"])
    df["diff_2_3"] = abs(df["d2"] - df["d3"])
    df["is_sequential"] = (
        ((df["d1"] + 1 == df["d2"]) & (df["d2"] + 1 == df["d3"])) |
        ((df["d1"] - 1 == df["d2"]) & (df["d2"] - 1 == df["d3"]))
    ).astype(int)
    df["modulo3_sum"] = df["sum_digits"] % 3

    return df


def prepare_data(df, top_n=100):
    feature_cols = [
        "month", "day", "weekday",
        "d1", "d2", "d3",
        "sum_digits", "has_double",
        "diff_1_2", "diff_2_3", "is_sequential", "modulo3_sum"
    ]
    X = df[feature_cols]
    y = df["3digits"].astype(str).str.zfill(3)

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # ✅ เลือกเฉพาะ top-N class ที่มีจำนวนมากที่สุด
    value_counts = pd.Series(y_encoded).value_counts()
    top_classes = value_counts.head(top_n).index

    mask = pd.Series(y_encoded).isin(top_classes)
    X_filtered = X[mask]
    y_filtered = pd.Series(y_encoded)[mask]

    if len(set(y_filtered)) < 2:
        print("⚠️ เหลือ class เดียวหลังกรอง ไม่สามารถ train ได้")
        return None, None, None, None

    try:
        return train_test_split(X_filtered, y_filtered, test_size=0.3, random_state=42, stratify=y_filtered)
    except ValueError:
        return train_test_split(X_filtered, y_filtered, test_size=0.3, random_state=42)



def tune_random_forest(X_train, y_train):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 400),
            'max_depth': trial.suggest_int('max_depth', 5, 30),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 5),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2']),
            'class_weight': trial.suggest_categorical('class_weight', ['balanced', 'balanced_subsample']),
            'random_state': 42,
            'n_jobs': -1
        }
        model = RandomForestClassifier(**params)
        return cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy').mean()

    print("🧪 Tuning Random Forest with Optuna...")
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=30, show_progress_bar=True)

    print("✅ Best RF Params:", study.best_params)
    return RandomForestClassifier(**study.best_params)

import os  # เพิ่มเข้ามา

def run_ml_pipeline(df):
    print("\n🚀 Running ML Pipeline...")

    if len(df) < 100:
        print("⚠️ ข้อมูลน้อยเกินไปสำหรับเทรน ML")
        return None

    df = feature_engineering(df)

    X_train, X_test, y_train, y_test = prepare_data(df, top_n=100)
    if X_train is None:
        return None

    # ========= Logistic Regression =========
    logreg = LogisticRegression(max_iter=2000, solver='saga', C=0.5)
    logreg.fit(X_train, y_train)
    logreg_pred = logreg.predict(X_test)
    logreg_acc = accuracy_score(y_test, logreg_pred)
    print("🔍 Logistic Regression Accuracy:", logreg_acc)

    # ========= Random Forest (Tuned) =========
    rf = tune_random_forest(X_train, y_train)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    print("🌲 Tuned Random Forest Accuracy:", rf_acc)

    # ========= XGBoost =========
    class_map = {old: new for new, old in enumerate(sorted(set(y_train)))}
    y_train_remap = y_train.map(class_map)
    y_test_remap = y_test.map(class_map)

    xgb_model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric='mlogloss',
        n_estimators=300,
        max_depth=10,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=1,
        reg_alpha=0.5,
        reg_lambda=1.0,
        random_state=42
    )
    xgb_model.fit(X_train, y_train_remap)
    xgb_pred = xgb_model.predict(X_test)
    xgb_acc = accuracy_score(y_test_remap, xgb_pred)
    print("⚡ XGBoost Accuracy:", xgb_acc)

    # ========= Classification Report =========
    print("\n📜 Classification Report (Logistic Regression):\n")
    print(classification_report(y_test, logreg_pred, zero_division=0))

    # ========= Save Models =========
    joblib.dump(logreg, "logreg_model.pkl")
    joblib.dump(xgb_model, "xgb_model.pkl")
    joblib.dump(rf, "rf_model.pkl")
    print("✅ Models saved: logreg_model.pkl, xgb_model.pkl, rf_model.pkl")

    # ========= Visualize Confusion Matrix (Random Forest) =========
    cm_rf = confusion_matrix(y_test, rf_pred)

    plt.figure(figsize=(10, 6))
    sns.heatmap(cm_rf[:20, :20], annot=True, fmt="d", cmap="Greens")
    plt.title("Confusion Matrix (Random Forest)")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()

    # ✅ Save instead of showing
    output_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    plot_path = os.path.join(output_dir, "confusion_matrix_rf.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"📦 Confusion matrix saved to: {plot_path}")

    # ✅ ส่ง accuracy กลับ (เอา xgb เป็นตัวแทนหลัก)
    return {
        "logreg": round(logreg_acc, 4),
        "rf": round(rf_acc, 4),
        "xgb": round(xgb_acc, 4)
    }


