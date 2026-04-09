from fastapi import FastAPI
 
app = FastAPI(
    title="Donor Bureau Pipeline",
    description="Excel to CSV donation data pipeline",
    version="0.1.0",
)
 
 
@app.get("/health")
def health_check():
    return {"status": "ok"}
 