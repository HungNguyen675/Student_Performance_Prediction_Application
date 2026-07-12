from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Student Performance Prediction API")

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the saved model pipeline
try:
    model = joblib.load('ensemble_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class StudentData(BaseModel):
    G1: float
    G2: float
    studytime: int
    failures: int
    absences: int
    schoolsup: str
    famsup: str
    paid: str
    higher: str
    internet: str
    freetime: int
    goout: int

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Performance Prediction API"}

@app.post("/predict")
def predict_performance(data: StudentData):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded correctly")
    
    # Convert input data to DataFrame
    input_df = pd.DataFrame([data.model_dump()])
    
    # The pipeline handles scaling and encoding internally
    predicted_score = model.predict(input_df)[0]
    
    # Calculate Rank based on Vietnamese Grading System
    if predicted_score >= 8.0:
        rank = "Giỏi"
        rank_id = 3
    elif predicted_score >= 6.5:
        rank = "Khá"
        rank_id = 2
    elif predicted_score >= 5.0:
        rank = "Trung Bình"
        rank_id = 1
    else:
        rank = "Yếu"
        rank_id = 0
        
    return {
        "score": round(float(predicted_score), 2),
        "rank": rank,
        "prediction": rank_id
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
