from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
from agent.agentic_workflow import AgenticWorkflow  # adjust path if needed

app = FastAPI()
agent = AgenticWorkflow()

class UserInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(data: UserInput):
    response = agent.run(data.message)
    return {"response": response}

@app.post("/chat/stream")
async def chat_stream(data: UserInput):
    def event_stream():
        for chunk in agent.stream_run(data.message):
            if "messages" in chunk:
                last = chunk["messages"][-1]
                yield f"data: {last.content if hasattr(last, 'content') else str(last)}\n\n"
            elif "error" in chunk:
                yield f"data: Error - {chunk['error']}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/")
def root():
    return {"message": "Travel Planner API is running!"}
