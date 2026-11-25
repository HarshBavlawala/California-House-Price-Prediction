from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# Frontend (HTML) ko backend se connect karne ke liye CORS allow karna
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Saved model aur pipeline load karna[cite: 39]
model = joblib.load("model.pkl")
pipeline = joblib.load("pipeline.pkl")

# Input data ka format
class HouseData(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str

@app.post("/predict")
def predict_price(data: HouseData):
    # Input ko DataFrame mein convert karna
    input_df = pd.DataFrame([data.dict()])
    
    # Pipeline se transform aur model se predict karna[cite: 39]
    transformed_data = pipeline.transform(input_df)
    prediction = model.predict(transformed_data)[0]
    
    return {"predicted_price": round(float(prediction), 2)}