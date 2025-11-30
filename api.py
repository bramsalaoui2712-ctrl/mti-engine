# api.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from cognitive_orchestrator import CognitiveOrchestrator

app = FastAPI(title="MTI Cognitive Engine API")
engine = CognitiveOrchestrator()

class UserInput(BaseModel):
    text: str

@app.post("/mti/process")
async def process_input(data: UserInput):
    result = await engine.process(data.text)
    return result

def start_api():
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=False)
