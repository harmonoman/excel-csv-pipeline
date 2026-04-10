from fastapi import FastAPI
from pathlib import Path
from app.config.loader import load_mapping_config, ConfigValidationError
 
CONFIG_PATH = Path(__file__).parent / "config" / "mapping.json"
 
# Fail fast — validate config at startup before accepting any requests
try:
    mapping_config = load_mapping_config(CONFIG_PATH)
except ConfigValidationError as e:
    raise RuntimeError(f"Invalid mapping config — pipeline cannot start: {e}")
 
app = FastAPI(
    title="Excel CSV Pipeline",
    description="Excel to CSV donation data pipeline",
    version="0.1.0",
)
 
 
@app.get("/health")
def health_check():
    return {"status": "ok"}
 