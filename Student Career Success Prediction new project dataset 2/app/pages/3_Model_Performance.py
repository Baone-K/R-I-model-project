# app/pages/3_📈_Model_Performance.py
import os
import sys
import streamlit as st
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared import load_model_results, load_feature_importance, load_model_artifacts, PREPARED_DIR

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")
st.markdown(
    """
    <style>
    .block-container { max-width: 1200px; padding: clamp(.75rem, 2vw, 1.5rem) clamp(.75rem, 3vw, 2rem); }
    @media (max-width: 640px) {
        h1 { font-size: 1.55rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.05rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📈 Model Performance")
st.caption("Evaluation of the Logistic Regression model used for 'Not Placed' risk prediction.")

@st.cache_data
def get_results():
    return load_model_results()

@st.cache_data
def get_feature_importance():
    return load_feature_importance()

results = get_results()
coefs = get_feature_importance()
model, threshold, columns = load_model_artifacts()

with st.expander("Deployment Configuration", expanded=True):
    c1, c2, c3 = st.columns(3, gap="small")
    c1.metric("Chosen Model", "Logistic Regression")
    c2.metric("Deployment Threshold", f"{float(threshold):.2f}")
    c3.metric("Features Used", f"{len(columns)}")

with st.expander("Model Comparison", expanded=True):
    st.caption("All 3 models evaluated at their CV-tuned thresholds.")
    display_cols = ["Model", "Threshold"]
    metric_cols = ["Precision (Not Placed)", "Recall (Not Placed)", "F1-Score (Not Placed)", "AUC-ROC"]
    available_metric_cols = [column for column in metric_cols if column in results.columns]
    st.dataframe(results[display_cols + available_metric_cols].style.format({column: "{:.4f}" for column in available_metric_cols}), use_container_width=True)
    if "F1-Score (Not Placed)" in results.columns:
        st.subheader("F1-Score by Model")
        fig = px.bar(results, x="Model", y="F1-Score (Not Placed)", text_auto=".3f", color="F1-Score (Not Placed)", color_continuous_scale="Blues")
        fig.update_layout(height=300, yaxis_title="F1-Score", coloraxis_showscale=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

with st.expander("Evaluation Curves"):
    image_files = [("ROC Curve", "roc_curve.png"), ("Confusion Matrix", "confusion_matrix.png"), ("Calibration Curve", "calibration_curve.png")]
    image_cols = st.columns(3, gap="small")
    for col, (title, filename) in zip(image_cols, image_files):
        with col:
            st.subheader(title)
            img_path = os.path.join(PREPARED_DIR, filename)
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.warning(f"Missing image: {filename}")

with st.expander("Feature Importance", expanded=True):
    if not coefs.empty:
        coefs_display = coefs.copy()
        coefs_display["abs_coef"] = coefs_display["Coefficient"].abs()
        top = coefs_display.sort_values("abs_coef", ascending=False).head(15).sort_values("Coefficient")
        fig = px.bar(top, x="Coefficient", y="Feature", orientation="h", color="Coefficient", color_continuous_scale="RdBu_r", text_auto=".3f")
        fig.update_layout(height=480, xaxis_title="Coefficient (+ increases 'Not Placed' risk)", yaxis_title="Feature", coloraxis_showscale=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.info("🎯 **Top drivers of 'Not Placed' risk:** Lower `Internships`, lower `CGPA`, and lower `Programming_Skill` increase the likelihood a student is not placed.")
    else:
        st.warning("pbi_feature_importance.csv not found.")

with st.expander("Interpretation Notes"):
    st.warning("**Calibration caveat:** Because `class_weight='balanced'` was used during training, the model's raw probabilities are not perfectly calibrated. **Interpret the output as a relative risk score for triage**, not as a true real-world percentage. AUC-ROC (0.80) confirms strong ranking ability.")
