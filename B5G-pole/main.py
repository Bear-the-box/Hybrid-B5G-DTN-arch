from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load("score_model.pkl")
app = FastAPI(title="B5G Score Prediction")

class NodeFeatures(BaseModel):
    timestamp: float
    host1: int
    host2: int
    duration: float
    buffer_availability: float
    battery_level: float
    contactedDestination: float

@app.get("/")
def read_root():
    return {"message": "Use POST /predict to get a score"}

@app.post("/predict")
def predict_score(data: NodeFeatures):
    features = np.array([[
        data.timestamp,
        data.host1,
        data.host2,
        data.duration,
        data.buffer_availability,
        data.battery_level,
        data.contactedDestination
    ]])

    # Predict score here
    prediction = model.predict(features)
    return {"predicted_score": float(prediction[0])}
