from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Data Log Processor")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
