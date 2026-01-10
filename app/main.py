from fastapi import FastAPI
from app.api.endpoints import router
from app.routers import predict

app = FastAPI(title="Data Log Processor")

app.include_router(router)
app.include_router(predict.router)

@app.get("/health")
def health():
    return {"status": "ok"}
