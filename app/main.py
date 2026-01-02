from fastapi import FastAPI

app = FastAPI(title="Data Processing API")

@app.get("/")
def health_check():
    return {"status": "ok"}
