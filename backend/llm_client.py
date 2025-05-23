# backend/api.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

from query_router import route_query  # Your backend logic router, implemented separately

app = FastAPI(title="Model Context Protocol Backend")

# CORS middleware to allow frontend calls (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "*"],  # Streamlit default ports plus wildcard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MCP Backend is running."}

@app.post("/query")
async def query(request: Request):
    """
    REST API endpoint for MCP query.
    Expects JSON body:
      {
        "prompt": "<user query string>",
        "client_type": "REST" | "SSE" | "STDIO"  (optional, defaults to REST)
      }
    Returns JSON:
      {
        "response": "<response string>"
      }
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    prompt = data.get("prompt")
    client_type = data.get("client_type", "REST").upper()

    if not prompt:
        raise HTTPException(status_code=400, detail="Missing 'prompt' field")

    # Call your query router to get response from LLM/tools
    response = await route_query(prompt, client_type)

    return {"response": response}

@app.get("/stream")
async def stream(request: Request):
    """
    SSE streaming endpoint.
    Accepts GET param 'prompt'.
    Streams partial responses as Server-Sent Events.
    """
    prompt = request.query_params.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="Missing 'prompt' query parameter")

    # We'll assume client_type SSE for streaming endpoint
    client_type = "SSE"

    async def event_generator():
        """
        Async generator that yields Server-Sent Events (SSE)
        from your backend's route_query in streaming mode.
        """
        # Your route_query should support streaming mode and yield chunks if needed.
        # For demo, simulate streaming response with fixed messages.
        # Replace this with actual async generator from your LLM or tool calls.
        chunks = [
            "Processing your request...",
            "Fetching data from tools...",
            f"Answer for: {prompt}"
        ]

        for chunk in chunks:
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(1)  # simulate delay

    return StreamingResponse(event_generator(), media_type="text/event-stream")
