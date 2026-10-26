# app/pages/3_📈_Model_Performance.py
import os
import sys
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared import (
    load_model_results,
    load_feature_importance,
    load_model_artifacts,
    PREPARED_DIR,
)

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")

st.title("📈 Model Performance")
st.markdown(
    "Evaluation of the Logistic Regression model used for 'Not Placed' risk prediction."
)


# ============================================================
# Load artifacts
# ============================================================
@st.cache_data
def get_results():
    return load_model_results()


@st.cache_data
def get_feature_importance():
    return load_feature_importance()


results = get_results()
coefs = get_feature_importance()
model, threshold, columns = load_model_artifacts()

# ============================================================
# Section 1: Deployment Info
# ============================================================
st.header("Deployment Configuration")
c1, c2, c3 = st.columns(3)
c1.metric("Chosen Model", "Logistic Regression")
c2.metric("Deployment Threshold", f"{float(threshold):.2f}")
c3.metric("Features Used", f"{len(columns)}")

# ============================================================
# Section 2: Model Comparison Table
# ============================================================
st.header("Model Comparison")
st.markdown("All 3 models evaluated at their CV-tuned thresholds:")

display_cols = ["Model", "Threshold"]
metric_cols = [
    "Precision (Not Placed)",
    "Recall (Not Placed)",
    "F1-Score (Not Placed)",
    "AUC-ROC",
]
available_metric_cols = [c for c in metric_cols if c in results.columns]

st.dataframe(
    results[display_cols + available_metric_cols].style.format(
        {c: "{:.4f}" for c in available_metric_cols}
    ),
    use_container_width=True,
)

# ============================================================
# Section 3: Metric comparison bar chart
# ============================================================
if "F1-Score (Not Placed)" in results.columns:
    st.subheader("F1-Score (Not Placed) by Model")
    fig = px.bar(
        results,
        x="Model",
        y="F1-Score (Not Placed)",
        text_auto=".3f",
        color="F1-Score (Not Placed)",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        height=350, yaxis_title="F1-Score", coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# Section 4: ROC / Confusion Matrix / Calibration (images)
# ============================================================
st.header("Evaluation Curves")

img_cols = st.columns(3)
image_files = [
    ("ROC Curve", "roc_curve.png"),
    ("Confusion Matrix", "confusion_matrix.png"),
    ("Calibration Curve", "calibration_curve.png"),
]

for col, (title, fname) in zip(img_cols, image_files):
    with col:
        st.subheader(title)
        img_path = os.path.join(PREPARED_DIR, fname)
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"Missing image: {fname}")

# ============================================================
# Section 5: Feature Importance
# ============================================================
st.header("Feature Importance (Logistic Regression Coefficients)")

if not coefs.empty:
    # Top 15 by absolute value
    coefs_display = coefs.copy()
    coefs_display["abs_coef"] = coefs_display["Coefficient"].abs()
    top = (
        coefs_display.sort_values("abs_coef", ascending=False)
        .head(15)
        .sort_values("Coefficient")
    )

    fig = px.bar(
        top,
        x="Coefficient",
        y="Feature",
        orientation="h",
        color="Coefficient",
        color_continuous_scale="RdBu_r",
        text_auto=".3f",
    )
    fig.update_layout(
        height=550,
        xaxis_title="Coefficient (+ increases 'Not Placed' risk)",
        yaxis_title="Feature",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "🎯 **Top drivers of 'Not Placed' risk:** "
        "Lower `Internships`, lower `CGPA`, and lower `Programming_Skill` "
        "increase the likelihood a student is not placed."
    )
else:
    st.warning("pbi_feature_importance.csv not found.")

# ============================================================
# Section 6: Summary note on calibration
# ============================================================
st.header("Interpretation Notes")
st.warning(
    "**Calibration caveat:** Because `class_weight='balanced'` was used during "
    "training, the model's raw probabilities are not perfectly calibrated. "
    "**Interpret the output as a relative risk score for triage**, not as a "
    "true real-world percentage. AUC-ROC (0.80) confirms strong ranking ability."
)