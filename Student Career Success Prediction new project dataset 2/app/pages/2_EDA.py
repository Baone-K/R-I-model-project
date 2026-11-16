# app/pages/2_🔍_EDA.py
import os
import sys
import streamlit as st
import plotly.express as px
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared import load_clean_data

st.set_page_config(page_title="EDA Explorer", page_icon="🔍", layout="wide")
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

@st.cache_data
def get_data():
    return load_clean_data()

df = get_data()
st.title("🔍 Exploratory Data Analysis")
st.caption("Explore how demographics, academics, and skills relate to placement.")

with st.expander("Demographics & Programme Analysis", expanded=True):
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.subheader("Placement Rate by Major")
        major_rates = df.groupby("Major")["placement_status_binary"].mean().sort_values().reset_index()
        fig = px.bar(major_rates, x="placement_status_binary", y="Major", orientation="h", text_auto=".1%", color="placement_status_binary", color_continuous_scale="Viridis")
        fig.update_layout(height=360, xaxis_title="Placement Rate", yaxis_title="", coloraxis_showscale=False, margin=dict(t=10, b=10))
        fig.update_xaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Placement Rate by Gender")
        gender_rates = df.groupby("Gender")["placement_status_binary"].mean().reset_index()
        fig = px.bar(gender_rates, x="Gender", y="placement_status_binary", text_auto=".1%", color="Gender", color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=210, xaxis_title="", yaxis_title="Placement Rate", showlegend=False, margin=dict(t=10, b=10))
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Placement Rate by University Year")
        order = ["Freshman", "Sophomore", "Junior", "Senior"]
        year_rates = df.groupby("University_Year")["placement_status_binary"].mean().reindex(order).reset_index()
        fig = px.bar(year_rates, x="University_Year", y="placement_status_binary", text_auto=".1%", color="placement_status_binary", color_continuous_scale="Blues")
        fig.update_layout(height=210, xaxis_title="", yaxis_title="Placement Rate", coloraxis_showscale=False, margin=dict(t=10, b=10))
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

with st.expander("Skills & Experience", expanded=True):
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.subheader("Placement Rate by Internships")
        int_rates = df.groupby("Internships")["placement_status_binary"].mean().reset_index()
        fig = px.bar(int_rates, x="Internships", y="placement_status_binary", text_auto=".0%", color="placement_status_binary", color_continuous_scale="Magma")
        fig.update_layout(height=290, xaxis_title="Internships", yaxis_title="Placement Rate", coloraxis_showscale=False, margin=dict(t=10, b=10))
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Placement Rate by Programming Skill")
        prog_rates = df.groupby("Programming_Skill")["placement_status_binary"].mean().reset_index()
        fig = px.bar(prog_rates, x="Programming_Skill", y="placement_status_binary", text_auto=".0%", color="placement_status_binary", color_continuous_scale="Cividis")
        fig.update_layout(height=290, xaxis_title="Skill Level (1-10)", yaxis_title="Placement Rate", coloraxis_showscale=False, margin=dict(t=10, b=10))
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("GitHub Profile")
    gh_rates = df.groupby("GitHub_Profile")["placement_status_binary"].mean().reset_index()
    fig = px.bar(gh_rates, x="GitHub_Profile", y="placement_status_binary", text_auto=".1%", color="GitHub_Profile", color_discrete_sequence=["#ef4444", "#22c55e"])
    fig.update_layout(height=260, xaxis_title="Has GitHub Profile", yaxis_title="Placement Rate", showlegend=False, margin=dict(t=10, b=10))
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Soft Skills & Academic Analysis"):
    col1, col2 = st.columns(2, gap="small")
    for container, feature, title, scale in [
        (col1, "Communication_Skills", "Communication Skills", "Blues"),
        (col2, "Teamwork", "Teamwork Skills", "Greens"),
    ]:
        with container:
            st.subheader(title)
            rates = df.groupby(feature)["placement_status_binary"].mean().reset_index()
            fig = px.bar(rates, x=feature, y="placement_status_binary", text_auto=".0%", color="placement_status_binary", color_continuous_scale=scale)
            fig.update_layout(height=260, xaxis_title="Skill Level (1-10)", yaxis_title="Placement Rate", coloraxis_showscale=False, margin=dict(t=10, b=10))
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.subheader("Problem Solving Skills")
        rates = df.groupby("Problem_Solving")["placement_status_binary"].mean().reset_index()
        fig = px.bar(rates, x="Problem_Solving", y="placement_status_binary", text_auto=".0%", color="placement_status_binary", color_continuous_scale="Oranges")
        fig.update_layout(height=260, xaxis_title="Skill Level (1-10)", yaxis_title="Placement Rate", coloraxis_showscale=False, margin=dict(t=10, b=10))
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Placement Rate by CGPA Band")
        cgpa_bands = pd.cut(df["CGPA"], bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0], labels=["< 2.0", "2.0 - 2.5", "2.5 - 3.0", "3.0 - 3.5", "3.5 - 4.0"])
        cgpa_rates = df.assign(CGPA_Band=cgpa_bands).groupby("CGPA_Band", observed=True)["placement_status_binary"].mean().reset_index()
        fig = px.bar(cgpa_rates, x="CGPA_Band", y="placement_status_binary", text_auto=".1%", color="placement_status_binary", color_continuous_scale="Purples")
        fig.update_layout(height=260, xaxis_title="CGPA Band", yaxis_title="Placement Rate", coloraxis_showscale=False, margin=dict(t=10, b=10))
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

with st.expander("Distributions & Correlation"):
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.subheader("CGPA Distribution")
        fig = px.histogram(df, x="CGPA", nbins=30, marginal="box", color_discrete_sequence=["teal"])
        fig.update_layout(height=280, xaxis_title="CGPA", yaxis_title="Count", margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Employability Score Distribution")
        fig = px.histogram(df, x="Employability_Score", nbins=30, marginal="box", color_discrete_sequence=["coral"])
        fig.update_layout(height=280, xaxis_title="Employability Score", yaxis_title="Count", margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Correlation Matrix (Pre-Placement Features Only)")
    st.caption("Excludes Resume Score, Interview Score, and Employability Score to prevent target leakage.")
    corr_cols = ["CGPA", "Attendance_Percentage", "Study_Hours_Per_Week", "Programming_Skill", "Projects_Completed", "Internships", "placement_status_binary"]
    corr_matrix = df[corr_cols].corr().round(2)
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    fig.update_layout(height=440, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.info("🎯 **Key Insight:** Internships (0.39) and Programming Skill (0.37) have the strongest positive correlation with placement.")
