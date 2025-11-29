from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from mti_engine import OperationalCognitiveOrchestrator

app = FastAPI()

# On crée l'orchestrateur global
system = OperationalCognitiveOrchestrator()
loop = asyncio.get_event_loop()

class UserInput(BaseModel):
    text: str

@app.post("/talk")
async def talk_to_engine(user_input: UserInput):
    result = await system.process_humanized_experience(
        {"input_text": user_input.text}
    )
    return {
        "response": result["decision"]["parameters"]["text"],
        "emotion": result["emotional_state"],
        "safety": result["safety_check"]
    }

@app.get("/")
def home():
    return {"status": "MTI Engine is running 🚀"}
