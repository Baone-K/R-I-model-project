# app/pages/1_📊_Dashboard.py
import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure `app` is importable from pages/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared import load_clean_data

st.set_page_config(page_title="Overview Dashboard", page_icon="📊", layout="wide")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def get_data():
    return load_clean_data()

df = get_data()

st.title("📊 Overview Dashboard")
st.markdown("High-level summary of student placement outcomes.")

# -----------------------------
# KPI Cards
# -----------------------------
total = len(df)
placed = int((df["placement_status_binary"] == 1).sum())
not_placed = int((df["placement_status_binary"] == 0).sum())
rate = placed / total

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", f"{total:,}")
c2.metric("Placement Rate", f"{rate:.2%}")
c3.metric("Placed", f"{placed:,}")
c4.metric("Not Placed", f"{not_placed:,}")

st.divider()

# -----------------------------
# Row 1: Placed vs Not Placed + Placement by Year
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Placed vs Not Placed")
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Placed", "Not Placed"],
                values=[placed, not_placed],
                hole=0.55,
                marker_colors=["#2563eb", "#f87171"],
                textinfo="label+percent",
            )
        ]
    )
    fig.update_layout(height=350, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Placement Rate by University Year")
    order = ["Freshman", "Sophomore", "Junior", "Senior"]
    year_rates = (
        df.groupby("University_Year")["placement_status_binary"]
        .mean()
        .reindex(order)
        .reset_index()
    )
    fig = px.bar(
        year_rates,
        x="University_Year",
        y="placement_status_binary",
        text_auto=".1%",
        color="placement_status_binary",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        height=350,
        xaxis_title="University Year",
        yaxis_title="Placement Rate",
        coloraxis_showscale=False,
    )
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Row 2: Internships + Programming Skill
# -----------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Placement Rate by Internships")
    int_rate = (
        df.groupby("Internships")["placement_status_binary"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        int_rate,
        x="Internships",
        y="placement_status_binary",
        text_auto=".1%",
        color="placement_status_binary",
        color_continuous_scale="Greens",
    )
    fig.update_layout(
        height=350,
        xaxis_title="Number of Internships",
        yaxis_title="Placement Rate",
        coloraxis_showscale=False,
    )
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Placement Rate by Programming Skill")
    prog_rate = (
        df.groupby("Programming_Skill")["placement_status_binary"]
        .mean()
        .reset_index()
    )
    fig = px.line(
        prog_rate,
        x="Programming_Skill",
        y="placement_status_binary",
        markers=True,
    )
    fig.update_layout(
        height=350,
        xaxis_title="Programming Skill Level (1-10)",
        yaxis_title="Placement Rate",
    )
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Row 3: Major distribution (treemap) + CGPA band
# -----------------------------
st.divider()
col5, col6 = st.columns(2)

with col5:
    st.subheader("Student Distribution by Major")
    major_counts = df.groupby("Major").size().reset_index(name="count")
    fig = px.treemap(
        major_counts,
        path=["Major"],
        values="count",
        color="count",
        color_continuous_scale="Teal",
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    st.subheader("Placement Rate by CGPA Band")
    df["CGPA_Band"] = pd.cut(
        df["CGPA"],
        bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0],
        labels=["< 2.0", "2.0-2.5", "2.5-3.0", "3.0-3.5", "3.5-4.0"],
    )
    cgpa_rate = (
        df.groupby("CGPA_Band", observed=True)["placement_status_binary"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        cgpa_rate,
        x="CGPA_Band",
        y="placement_status_binary",
        text_auto=".1%",
        color="placement_status_binary",
        color_continuous_scale="Purples",
    )
    fig.update_layout(
        height=400,
        xaxis_title="CGPA Band",
        yaxis_title="Placement Rate",
        coloraxis_showscale=False,
    )
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)