"""
Simple FastAPI server to serve the UI and handle fact-checking requests
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from src.orchestration.graph import create_graph
from src.utils import load_env

# Load environment variables (API keys)
load_env()

app = FastAPI(title="Fact Checker UI Server")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StatementRequest(BaseModel):
    statement: str

class FactCheckResponse(BaseModel):
    verdict: str
    reasoning: str

@app.get("/")
async def root():
    """Serve the index.html"""
    return FileResponse("ui/index.html")

@app.post("/check", response_model=FactCheckResponse)
async def check_fact(request: StatementRequest):
    """Check a fact using the agent"""
    print(f"Received request: {request.statement}")
    try:
        graph = create_graph()
        initial_state = {"statement": request.statement}
        
        print("Invoking graph...")
        result = await graph.ainvoke(initial_state)
        print("Graph execution successful!")
        
        return FactCheckResponse(
            verdict=result["verdict"],
            reasoning=result["verification_reasoning"]
        )
    except Exception as e:
        print(f"ERROR executing graph: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting Fact Checker UI Server...")
    print("Open your browser to: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
