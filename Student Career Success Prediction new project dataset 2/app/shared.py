# app/shared.py
import os
import pandas as pd
import joblib

# Resolve project root (two levels up from app/pages or app/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PREPARED_DIR = os.path.join(BASE_DIR, "prepared_data")
MODELS_DIR = os.path.join(BASE_DIR, "models")


def load_clean_data() -> pd.DataFrame:
    """Load the cleaned dataset from prepared_data/."""
    return pd.read_csv(os.path.join(PREPARED_DIR, "clean_data.csv"))


def load_model_artifacts():
    """Load the trained model, threshold, and expected columns."""
    model = joblib.load(os.path.join(MODELS_DIR, "best_model.pkl"))
    threshold = joblib.load(os.path.join(MODELS_DIR, "chosen_threshold.pkl"))
    columns = joblib.load(os.path.join(MODELS_DIR, "training_columns.pkl"))
    return model, threshold, columns


def load_model_results() -> pd.DataFrame:
    """Load the Power BI model results CSV."""
    return pd.read_csv(os.path.join(PREPARED_DIR, "pbi_model_results.csv"))


def load_feature_importance() -> pd.DataFrame:
    """Load the Power BI feature importance CSV."""
    return pd.read_csv(os.path.join(PREPARED_DIR, "pbi_feature_importance.csv"))