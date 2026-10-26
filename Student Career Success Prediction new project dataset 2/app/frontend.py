# app/frontend.py
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Graduate Placement Predictor", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Segoe UI', sans-serif; }
    p { color: #A0AEC0 !important; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stSelectbox label, .stSlider label { color: #E2E8F0 !important; font-weight: 500; }
    div[data-testid="stVerticalBlock"] > div { background-color: #1A202C; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stButton>button { background-color: #2B6CB0; color: white; border-radius: 8px; border: none; padding: 10px 24px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #3182CE; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Graduate Placement Predictor")
st.write("Enter a student's profile to predict their placement outcome. This tool relies strictly on **pre-placement features**.")

with st.container():
    st.header("Student Profile")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Academics")
        gender = st.selectbox("Gender", ["Male", "Female"], index=0)
        cgpa = st.slider("CGPA", 0.0, 4.0, 3.0, step=0.1) 
        attendance = st.slider("Attendance Percentage", 0, 100, 85) 
        study_hours = st.slider("Study Hours / Week", 0, 40, 15)
        uni_year = st.selectbox("University Year", ["Freshman", "Sophomore", "Junior", "Senior"], index=3)
        major = st.selectbox("Major", ["Computer Science", "Information Technology", "Software Engineering", "Data Science", "Artificial Intelligence", "Cybersecurity", "Electrical Engineering", "Business Analytics"])
        
    with col2:
        st.subheader("Skills")
        prog_skill = st.slider("Programming Skill (1-10)", 1, 10, 7) 
        comm_skill = st.slider("Communication Skills (1-10)", 1, 10, 7) 
        teamwork = st.slider("Teamwork (1-10)", 1, 10, 7) 
        problem_solving = st.slider("Problem Solving (1-10)", 1, 10, 7) 
        english = st.selectbox("English Proficiency", ["Basic", "Intermediate", "Advanced"], index=2)
        
    with col3:
        st.subheader("Experience & Context")
        internships = st.slider("Internships Completed", 0, 5, 1) 
        projects = st.slider("Projects Completed", 0, 10, 3) 
        certs = st.slider("Certifications", 0, 10, 1) 
        hackathons = st.slider("Hackathons", 0, 10, 0)
        github = st.selectbox("Has GitHub Profile?", ["Yes", "No"], index=0)
        linkedin = st.selectbox("Has LinkedIn Profile?", ["Yes", "No"], index=0)
        leadership = st.selectbox("Leadership Experience?", ["Yes", "No"], index=1)
        
    st.markdown("---")
    submit = st.button("Predict Placement")

if submit:
    API_URL = "http://127.0.0.1:8000/predict"
    
    payload = {
        "Gender": gender, "University_Year": uni_year, "Major": major, "Attendance_Percentage": attendance,
        "Study_Hours_Per_Week": study_hours, "CGPA": float(cgpa), "Programming_Skill": prog_skill,
        "Projects_Completed": projects, "Certifications": certs, "Hackathons": hackathons,
        "GitHub_Profile": github, "Internships": internships, "Leadership_Experience": leadership,
        "LinkedIn_Profile": linkedin, "Communication_Skills": comm_skill, "Teamwork": teamwork,
        "Problem_Solving": problem_solving, "English_Proficiency": english
    }
    
    try:
        with st.spinner("Analyzing profile..."):
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                st.markdown("---")
                st.subheader("Prediction Result")
                
                status = result['prediction']
                prob_not_placed = result['probability_not_placed'] * 100
                prob_placed = result['probability_placed'] * 100
                
                # --- DETERMINE UI BANDS ---
                if status == "Placed":
                    risk_band = "Low Risk"
                    band_color = "#22543D" 
                    text_color = "#9AE6B4"
                    status_msg = f"The model predicts a strong {prob_placed:.1f}% chance of placement."
                    display_score = prob_placed
                    score_label = "Placement Probability"
                else:
                    if prob_not_placed >= 75:
                        risk_band = "High Risk"
                        band_color = "#742A2A" 
                        text_color = "#FEB2B2"
                    else:
                        risk_band = "Moderate Risk"
                        band_color = "#744210" 
                        text_color = "#FBD38D"
                    status_msg = f"The model predicts only a {prob_placed:.1f}% chance of placement ({prob_not_placed:.1f}% risk score). Intervention recommended."
                    display_score = prob_not_placed
                    score_label = "Risk Score (Not Placed)"

                # --- MAIN RESULT CARD ---
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                        <div style="flex: 1;">
                            <p style="margin-bottom: 5px; font-size: 14px; color: #A0AEC0;">Predicted Status</p>
                            <h2 style="margin: 0; color: #FFFFFF;">{status}</h2>
                        </div>
                        <div style="flex: 1;">
                            <p style="margin-bottom: 5px; font-size: 14px; color: #A0AEC0;">{score_label}</p>
                            <h2 style="margin: 0; color: #FFFFFF;">{display_score:.1f}%</h2>
                        </div>
                        <div style="flex: 1;">
                            <p style="margin-bottom: 5px; font-size: 14px; color: #A0AEC0;">Risk Band</p>
                            <h2 style="margin: 0; color: #FFFFFF;">{risk_band}</h2>
                        </div>
                    </div>
                    
                    <div style="background-color: {band_color}; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <p style="margin: 0; color: {text_color}; font-weight: 600;">{status_msg}</p>
                    </div>
                """, unsafe_allow_html=True)

                # --- FEATURE CONTRIBUTIONS (THE "WHY") ---
                st.markdown("### 🔍 Key Drivers for this Prediction")
                st.write("Here is how specific features in the student's profile impacted the final decision:")
                
                top_factors = result.get('top_factors', {})
                
                cols = st.columns(len(top_factors))
                for idx, (feature, impact) in enumerate(top_factors.items()):
                    with cols[idx]:
                        if impact > 0:
                            st.metric(label=feature, value="Increases Risk", delta=f"{impact:.2f}", delta_color="inverse")
                        else:
                            st.metric(label=feature, value="Reduces Risk", delta=f"{impact:.2f}", delta_color="normal")

                # --- NEW: ACTIONABLE RECOMMENDATIONS ---
                st.markdown("### 💡 How to Improve Placement Chances")
                st.write("Based on the model's rules, here are the most impactful actions this student can take:")
                
                recommendations = []
                
                # Check weak points based on the dataset's strongest features
                if internships < 2:
                    recommendations.append("**Get an Internship:** The model heavily penalizes students with fewer than 2 internships. Securing an industry internship is the single most powerful way to reduce risk.")
                if projects < 3:
                    recommendations.append("**Build More Projects:** Aim for 3-5 end-to-end projects. Practical proof of work heavily influences placement.")
                if prog_skill < 7:
                    recommendations.append("**Improve Programming Skills:** Low coding scores are a major red flag. Practice consistently on platforms like LeetCode or HackerRank.")
                if hackathons == 0:
                    recommendations.append("**Participate in Hackathons:** Even participating (without winning) shows initiative and teamwork to employers.")
                if leadership == "No":
                    recommendations.append("**Seek Leadership Roles:** Take up a committee role or lead a group project to build leadership experience.")
                if github == "No":
                    recommendations.append("**Create a GitHub Profile:** Showcase your code publicly. Employers look for this.")
                if attendance < 75:
                    recommendations.append("**Improve Attendance:** Low attendance correlates with lower academic engagement and is a negative signal to employers.")
                
                # If the student is already perfect, congratulate them
                if not recommendations:
                    st.success("🌟 Excellent profile! This student is already meeting all the key criteria for placement. Focus on interview preparation and networking.")
                else:
                    for rec in recommendations:
                        st.info(rec)

                with st.expander("🛠️ View Full API Debug Data"):
                    st.write(f"**Model's Threshold for 'Not Placed':** {result['threshold_used']}")
                    debug_df = pd.DataFrame(list(result['debug_features'].items()), columns=['Feature Name', 'Value'])
                    st.dataframe(debug_df, hide_index=True, use_container_width=True)

            else:
                st.error(f"Error from API: {response.text}")
                
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Make sure your FastAPI server is running in a separate terminal (`python -m uvicorn app.main:app --reload`).")