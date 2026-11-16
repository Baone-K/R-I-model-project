# app/frontend.py
import os
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Interface", page_icon="🎓", layout="wide")

# Keep the interface responsive without overriding Streamlit's active theme colors.
st.markdown(
    """
    <style>
    .block-container {
        width: 100%;
        max-width: 1200px;
        padding-top: clamp(1rem, 3vw, 2rem);
        padding-bottom: 2rem;
        padding-left: clamp(1rem, 4vw, 3rem);
        padding-right: clamp(1rem, 4vw, 3rem);
    }
    [data-testid="stMetric"] { min-width: 0; }
    @media (max-width: 640px) {
        h1 { font-size: 1.7rem !important; }
        h2 { font-size: 1.35rem !important; }
        [data-testid="stSlider"] { padding-bottom: .35rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎓 Graduate Placement Predictor")
st.write(
    "Enter a student's profile to predict their placement outcome. "
    "This tool relies strictly on **pre-placement features**."
)

with st.container(border=True):
    st.header("Student Profile")
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.subheader("Academics")
        gender = st.selectbox("Gender", ["Male", "Female"], index=0)
        cgpa = st.slider("CGPA", 0.0, 4.0, 3.0, step=0.1)
        attendance = st.slider("Attendance Percentage", 0, 100, 85)
        study_hours = st.slider("Study Hours / Week", 0, 40, 15)
        uni_year = st.selectbox(
            "University Year",
            ["Freshman", "Sophomore", "Junior", "Senior"],
            index=3,
        )
        major = st.selectbox(
            "Major",
            [
                "Computer Science",
                "Information Technology",
                "Software Engineering",
                "Data Science",
                "Artificial Intelligence",
                "Cybersecurity",
                "Electrical Engineering",
                "Business Analytics",
            ],
        )

    with col2:
        st.subheader("Skills")
        prog_skill = st.slider("Programming Skill (1-10)", 1, 10, 7)
        comm_skill = st.slider("Communication Skills (1-10)", 1, 10, 7)
        teamwork = st.slider("Teamwork (1-10)", 1, 10, 7)
        problem_solving = st.slider("Problem Solving (1-10)", 1, 10, 7)
        english = st.selectbox(
            "English Proficiency", ["Basic", "Intermediate", "Advanced"], index=2
        )

    with col3:
        st.subheader("Experience & Context")
        internships = st.slider("Internships Completed", 0, 5, 1)
        projects = st.slider("Projects Completed", 0, 10, 3)
        certs = st.slider("Certifications", 0, 10, 1)
        hackathons = st.slider("Hackathons", 0, 10, 0)
        github = st.selectbox("Has GitHub Profile?", ["Yes", "No"], index=0)
        linkedin = st.selectbox("Has LinkedIn Profile?", ["Yes", "No"], index=0)
        leadership = st.selectbox(
            "Leadership Experience?", ["Yes", "No"], index=1
        )

    st.divider()
    submit = st.button("Predict Placement", type="primary", use_container_width=True)

if submit:
    api_url = os.getenv(
        "PLACEMENT_API_URL", "https://r-i-model-project-1.onrender.com/predict"
    )
    payload = {
        "Gender": gender,
        "University_Year": uni_year,
        "Major": major,
        "Attendance_Percentage": attendance,
        "Study_Hours_Per_Week": study_hours,
        "CGPA": float(cgpa),
        "Programming_Skill": prog_skill,
        "Projects_Completed": projects,
        "Certifications": certs,
        "Hackathons": hackathons,
        "GitHub_Profile": github,
        "Internships": internships,
        "Leadership_Experience": leadership,
        "LinkedIn_Profile": linkedin,
        "Communication_Skills": comm_skill,
        "Teamwork": teamwork,
        "Problem_Solving": problem_solving,
        "English_Proficiency": english,
    }

    try:
        with st.spinner("Analyzing profile..."):
            response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        st.divider()
        st.subheader("Prediction Result")
        status = result["prediction"]
        prob_not_placed = result["probability_not_placed"] * 100
        prob_placed = result["probability_placed"] * 100

        if status == "Placed":
            risk_band = "Low Risk"
            status_msg = f"The model predicts a {prob_placed:.1f}% chance of placement."
            display_score = prob_placed
            score_label = "Placement Probability"
            st.success(status_msg)
        else:
            risk_band = "High Risk" if prob_not_placed >= 75 else "Moderate Risk"
            status_msg = (
                f"The model predicts a {prob_placed:.1f}% chance of placement "
                f"({prob_not_placed:.1f}% risk score). Intervention recommended."
            )
            display_score = prob_not_placed
            score_label = "Risk Score (Not Placed)"
            st.warning(status_msg)

        result_cols = st.columns(3, gap="medium")
        result_cols[0].metric("Predicted Status", status)
        result_cols[1].metric(score_label, f"{display_score:.1f}%")
        result_cols[2].metric("Risk Band", risk_band)

        st.markdown("### 🔍 Key Drivers for this Prediction")
        st.write(
            "These features contributed most to the model's decision. "
            "Positive values increase estimated not-placed risk; negative values reduce it."
        )
        top_factors = result.get("top_factors") or {}
        if top_factors:
            factor_cols = st.columns(min(len(top_factors), 2), gap="medium")
            for idx, (feature, impact) in enumerate(top_factors.items()):
                with factor_cols[idx % len(factor_cols)]:
                    direction = "Increases Risk" if impact > 0 else "Reduces Risk"
                    color = "inverse" if impact > 0 else "normal"
                    st.metric(
                        label=feature,
                        value=direction,
                        delta=f"{impact:.2f}",
                        delta_color=color,
                    )

        st.markdown("### 💡 How to Improve Placement Chances")
        recommendations = []
        if internships < 2:
            recommendations.append(
                "**Get an Internship:** Seek industry experience to build practical skills."
            )
        if projects < 3:
            recommendations.append(
                "**Build More Projects:** Aim for 3-5 end-to-end projects that demonstrate practical work."
            )
        if prog_skill < 7:
            recommendations.append(
                "**Improve Programming Skills:** Practice consistently and build projects to strengthen coding skills."
            )
        if hackathons == 0:
            recommendations.append(
                "**Participate in Hackathons:** Build initiative and teamwork through practical challenges."
            )
        if leadership == "No":
            recommendations.append(
                "**Seek Leadership Roles:** Lead a group project or take on a team role."
            )
        if github == "No":
            recommendations.append(
                "**Create a GitHub Profile:** Showcase projects and code in a public portfolio."
            )
        if attendance < 75:
            recommendations.append(
                "**Improve Attendance:** Consistent attendance supports academic engagement."
            )

        if recommendations:
            for recommendation in recommendations:
                st.info(recommendation)
        else:
            st.success(
                "🌟 Excellent profile! Keep preparing for interviews and building your professional network."
            )

        with st.expander("🛠️ View Full API Debug Data"):
            st.write(f"**Model threshold for 'Not Placed':** {result['threshold_used']}")
            debug_df = pd.DataFrame(
                list(result.get("debug_features", {}).items()),
                columns=["Feature Name", "Value"],
            )
            st.dataframe(debug_df, hide_index=True, use_container_width=True)

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the prediction API. Please try again later or check that the API is running."
        )
    except requests.exceptions.Timeout:
        st.error("The prediction API took too long to respond. Please try again.")
    except requests.exceptions.HTTPError as error:
        st.error(f"The prediction API returned an error: {error}")
    except (requests.exceptions.RequestException, ValueError, KeyError) as error:
        st.error(f"Could not complete the prediction: {error}")
