"""HTTP API for the fortune-teller agent."""

from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from agent import build_agent, tools_used

app = FastAPI(title="Madame Mystica", description="A fortune-teller agent 🔮")
agent = build_agent()


class Question(BaseModel):
    question: str


class Prediction(BaseModel):
    prediction: str
    tools_used: list[str]


@app.get("/health")
def health() -> dict:
    """Liveness check."""
    return {"status": "ok"}


@app.post("/predict", response_model=Prediction)
def predict(body: Question) -> Prediction:
    """Return a single prediction for the given question."""
    result = agent.invoke({"messages": [HumanMessage(content=body.question)]})
    messages = result["messages"]
    return Prediction(prediction=messages[-1].content, tools_used=tools_used(messages))