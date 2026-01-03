from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    df = pd.read_csv(file.file)

    return {
        "rows": len(df),
        "columns": list(df.columns)
    }

@router.post("/profile-csv")
async def profile_csv(file: UploadFile = File(...)):
    # 1. Validación de tipo
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=415,
            detail="Only CSV files are supported"
        )

    try:
        # 2. Leer CSV
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file"
        )

    # 3. Validar vacío
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="CSV file is empty"
        )

    profile = {}

    # 4. Profiling por columna
    for col in df.columns:
        series = df[col]

        if pd.api.types.is_numeric_dtype(series):
            profile[col] = {
                "type": "numeric",
                "nulls": int(series.isna().sum()),
                "min": float(series.min()),
                "max": float(series.max()),
                "mean": float(series.mean())
            }
        else:
            profile[col] = {
                "type": "string",
                "nulls": int(series.isna().sum()),
                "unique": int(series.nunique())
            }

    return {
        "rows": int(len(df)),
        "columns": profile
    }
