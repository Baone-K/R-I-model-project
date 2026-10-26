# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
import pandas as pd
import numpy as np
import joblib
import os

app = FastAPI(
    title="Graduate Employability Prediction API",
    description="Predicts student placement status with feature contribution analysis.",
    version="9.0.0"
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Load artifacts
model = joblib.load(os.path.join(MODELS_DIR, 'best_model.pkl'))
training_columns = joblib.load(os.path.join(MODELS_DIR, 'training_columns.pkl'))
CHOSEN_THRESHOLD = float(joblib.load(os.path.join(MODELS_DIR, 'chosen_threshold.pkl'))) 

class StudentData(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Gender": "Male", "University_Year": "Senior", "Major": "Computer Science",
                "Attendance_Percentage": 85, "Study_Hours_Per_Week": 15, "CGPA": 3.0,
                "Programming_Skill": 7, "Projects_Completed": 3, "Certifications": 1,
                "Hackathons": 0, "GitHub_Profile": "Yes", "Internships": 1,
                "Leadership_Experience": "No", "LinkedIn_Profile": "Yes", 
                "Communication_Skills": 7, "Teamwork": 7, "Problem_Solving": 7, 
                "English_Proficiency": "Advanced"
            }
        }
    )
    Gender: str
    University_Year: str
    Major: str
    Attendance_Percentage: int
    Study_Hours_Per_Week: int
    CGPA: float
    Programming_Skill: int
    Projects_Completed: int
    Certifications: int
    Hackathons: int
    GitHub_Profile: str
    Internships: int
    Leadership_Experience: str
    LinkedIn_Profile: str
    Communication_Skills: int
    Teamwork: int
    Problem_Solving: int
    English_Proficiency: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Graduate Employability Prediction API"}

@app.post("/predict")
def predict_placement(data: StudentData):
    # 1. Convert input to DataFrame
    df = pd.DataFrame([data.model_dump()])
    
    # 2. One-hot encode
    df_encoded = pd.get_dummies(df, drop_first=True, dtype=int)
    
    # 3. Align with training columns
    df_final = df_encoded.reindex(columns=training_columns, fill_value=0)
    
    # 4. Get probabilities
    probabilities = model.predict_proba(df_final)[0]
    placed_idx = list(model.classes_).index(0)
    prob_placed = float(probabilities[placed_idx])
    prob_not_placed = 1.0 - prob_placed
    
    # 5. Determine prediction based on threshold for 'Not Placed'
    is_not_placed = prob_not_placed >= CHOSEN_THRESHOLD
    prediction_label = "Not Placed" if is_not_placed else "Placed"
    
    # 6. Feature Contribution Analysis (Why did the model decide this?)
    # We multiply the model's coefficients by the student's input values
    feature_impacts = {}
    coefs = model.coef_[0]
    
    for i, col in enumerate(training_columns):
        val = df_final[col].iloc[0]
        # If the feature is present (e.g., 1 for one-hot, or the actual number for CGPA)
        if val != 0:
            impact = coefs[i] * val
            # Clean up feature names for the UI
            clean_name = col.replace('_', ' ')
            feature_impacts[clean_name] = float(impact)
            
    # Sort impacts: Positive means it pushed towards "Not Placed", Negative towards "Placed"
    sorted_impacts = dict(sorted(feature_impacts.items(), key=lambda item: abs(item[1]), reverse=True))
    
    # Grab the top 4 driving factors
    top_factors = dict(list(sorted_impacts.items())[:4])

    return {
        "prediction": prediction_label,
        "probability_placed": prob_placed,
        "probability_not_placed": prob_not_placed,
        "threshold_used": CHOSEN_THRESHOLD,
        "top_factors": top_factors, # New: Explains the "Why"
        "debug_features": df_final.to_dict(orient="records")[0]
    }