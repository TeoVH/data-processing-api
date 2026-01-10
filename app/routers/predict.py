from fastapi import APIRouter, HTTPException
from app.schemas.predict import PredictInput
import numpy as np
import joblib
import os

router = APIRouter()

MODEL_PATH = "models/linear_regression.joblib"

@router.post("/predict")
def predict(data: PredictInput):

    # 1. Verificar modelo
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=500,
            detail="Model not found. Train the model first."
        )

    # 2. Cargar modelo
    model = joblib.load(MODEL_PATH)

    # 3. Preparar input (MISMO orden que entrenamiento)
    X = np.array([[
        data.Latitude,
        data.Longitude
    ]])

    # 4. Predicción
    prediction = model.predict(X)[0]

    # 5. Validar resultado
    if not np.isfinite(prediction):
        raise HTTPException(
            status_code=400,
            detail="Invalid prediction result"
        )

    return {
        "predicted_population": float(prediction),
        "status": "prediction successful"
    }
