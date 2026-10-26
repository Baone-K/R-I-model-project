# app/pages/2_🔍_EDA.py
import os
import sys
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Ensure `app` is importable from pages/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared import load_clean_data

st.set_page_config(page_title="EDA Explorer", page_icon="🔍", layout="wide")

@st.cache_data
def get_data():
    return load_clean_data()

df = get_data()

st.title("🔍 Exploratory Data Analysis")
st.markdown("Interactive exploration of how demographics, academics, and skills relate to placement.")

# ============================================================
# 1. Demographics & Programme Analysis
# ============================================================
st.header("1. Demographics & Programme Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Employment Rate by Programme (Major)")
    # Sorted descending, horizontal bar
    major_rates = df.groupby('Major')['placement_status_binary'].mean().sort_values(ascending=True).reset_index()
    fig = px.bar(
        major_rates, x='placement_status_binary', y='Major', orientation='h',
        text_auto='.1%', color='placement_status_binary', color_continuous_scale='Viridis'
    )
    fig.update_layout(height=450, xaxis_title="Placement Rate", yaxis_title="", coloraxis_showscale=False)
    fig.update_xaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Employment Rate by Gender")
    gender_rates = df.groupby('Gender')['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        gender_rates, x='Gender', y='placement_status_binary', text_auto='.1%',
        color='Gender', color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(height=220, xaxis_title="", yaxis_title="Placement Rate", showlegend=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Employment Rate by University Year")
    order = ['Freshman', 'Sophomore', 'Junior', 'Senior']
    year_rates = df.groupby('University_Year')['placement_status_binary'].mean().reindex(order).reset_index()
    fig = px.bar(
        year_rates, x='University_Year', y='placement_status_binary', text_auto='.1%',
        color='placement_status_binary', color_continuous_scale='Blues'
    )
    fig.update_layout(height=220, xaxis_title="", yaxis_title="Placement Rate", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================================================
# 2. Skills, Experience & Placement
# ============================================================
st.header("2. Skills & Experience")

col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("Internship Experience")
    int_rates = df.groupby('Internships')['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        int_rates, x='Internships', y='placement_status_binary', text_auto='.0%',
        color='placement_status_binary', color_continuous_scale='Magma'
    )
    fig.update_layout(height=350, xaxis_title="Internships", yaxis_title="Placement Rate", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Programming Skills")
    prog_rates = df.groupby('Programming_Skill')['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        prog_rates, x='Programming_Skill', y='placement_status_binary', text_auto='.0%',
        color='placement_status_binary', color_continuous_scale='Cividis'
    )
    fig.update_layout(height=350, xaxis_title="Skill Level (1-10)", yaxis_title="", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with col5:
    st.subheader("GitHub Profile")
    gh_rates = df.groupby('GitHub_Profile')['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        gh_rates, x='GitHub_Profile', y='placement_status_binary', text_auto='.1%',
        color='GitHub_Profile', color_discrete_sequence=['#ef4444', '#22c55e']
    )
    fig.update_layout(height=350, xaxis_title="Has GitHub Profile", yaxis_title="", showlegend=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Impact of Programming Skills (Line Trend)")
fig = px.line(
    prog_rates, x='Programming_Skill', y='placement_status_binary', markers=True,
    labels={'Programming_Skill': 'Programming Skill Level', 'placement_status_binary': 'Placement Rate'}
)
fig.update_layout(height=350, yaxis_tickformat=".0%")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================================================
# 3. Soft Skills & Academic Analysis
# ============================================================
st.header("3. Soft Skills & Academic Analysis")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Impact of Communication Skills")
    comm_rates = df.groupby('Communication_Skills')['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        comm_rates, x='Communication_Skills', y='placement_status_binary', text_auto='.0%',
        color='placement_status_binary', color_continuous_scale='Blues'
    )
    fig.update_layout(height=300, xaxis_title="Skill Level (1-10)", yaxis_title="Placement Rate", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Impact of Problem Solving Skills")
    prob_rates = df.groupby('Problem_Solving')['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        prob_rates, x='Problem_Solving', y='placement_status_binary', text_auto='.0%',
        color='placement_status_binary', color_continuous_scale='Oranges'
    )
    fig.update_layout(height=300, xaxis_title="Skill Level (1-10)", yaxis_title="Placement Rate", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with row2_col2:
    st.subheader("Impact of Teamwork Skills")
    team_rates = df.groupby('Teamwork')['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        team_rates, x='Teamwork', y='placement_status_binary', text_auto='.0%',
        color='placement_status_binary', color_continuous_scale='Greens'
    )
    fig.update_layout(height=300, xaxis_title="Skill Level (1-10)", yaxis_title="Placement Rate", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Impact of CGPA Bands")
    # Create a temporary CGPA band
    df['CGPA_Band'] = pd.cut(
        df['CGPA'], bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0], 
        labels=['< 2.0', '2.0 - 2.5', '2.5 - 3.0', '3.0 - 3.5', '3.5 - 4.0']
    )
    cgpa_rates = df.groupby('CGPA_Band', observed=True)['placement_status_binary'].mean().reset_index()
    fig = px.bar(
        cgpa_rates, x='CGPA_Band', y='placement_status_binary', text_auto='.1%',
        color='placement_status_binary', color_continuous_scale='Purples'
    )
    fig.update_layout(height=300, xaxis_title="CGPA Band", yaxis_title="Placement Rate", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
    
    # Drop the temp column
    df = df.drop(columns=['CGPA_Band'])

st.divider()

# ============================================================
# 4. Univariate Analysis & Correlation
# ============================================================
st.header("4. Univariate Analysis & Correlation")

col6, col7 = st.columns(2)

with col6:
    st.subheader("Distribution of CGPA")
    fig = px.histogram(df, x='CGPA', nbins=40, marginal='box', color_discrete_sequence=['teal'])
    fig.update_layout(height=350, xaxis_title="CGPA", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

with col7:
    st.subheader("Distribution of Employability Score")
    fig = px.histogram(df, x='Employability_Score', nbins=40, marginal='box', color_discrete_sequence=['coral'])
    fig.update_layout(height=350, xaxis_title="Employability Score", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Correlation Matrix (Pre-Placement Features Only)")
st.markdown("Excludes Resume Score, Interview Score, and Employability Score to prevent target leakage.")

corr_cols = [
    'CGPA', 'Attendance_Percentage', 'Study_Hours_Per_Week',
    'Programming_Skill', 'Projects_Completed', 'Internships', 'placement_status_binary'
]
corr_matrix = df[corr_cols].corr().round(2)

fig = px.imshow(
    corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1
)
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

st.info("🎯 **Key Insight:** Internships (0.39) and Programming Skill (0.37) have the strongest positive correlation with placement.")