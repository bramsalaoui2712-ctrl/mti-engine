from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from cognitive_orchestrator import CognitiveOrchestrator

app = FastAPI(title="MTI Engine API", version="1.0")

orchestrator = CognitiveOrchestrator()

class Query(BaseModel):
    text: str

@app.post("/ask")
async def ask(query: Query):
    result = await orchestrator.process_user_input(query.text)
    return result

@app.get("/")
def root():
    return {"status": "MTI Engine operational"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
