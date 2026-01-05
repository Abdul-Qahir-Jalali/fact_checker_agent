"""
Hybrid FastMCP + FastAPI Server
Uses FastMCP for tool definitions but exposes via FastAPI REST for compatibility
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os

# Initialize FastMCP for tool management
mcp = FastMCP("Tavily Search Server")

# Initialize FastAPI for HTTP endpoints
app = FastAPI(title="Fact Checker MCP Server")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Tavily Client
tavily_api_key = os.getenv("TAVILY_API_KEY", "").strip()
print(f"DEBUG: Server loaded. Tavily API Key: {'YES' if tavily_api_key else 'NO'}")
if tavily_api_key:
    print(f"DEBUG: Key starts with: {tavily_api_key[:3]}...")

tavily = TavilyClient(api_key=tavily_api_key)

# Define FastMCP tool (clean syntax!)
@mcp.tool()
def search(query: str, count: int = 3) -> str:
    """
    Perform a web search using Tavily.
    Args:
        query: The search query.
        count: Number of results to return.
    """
    print(f"Processing search: {query}")
    try:
        response = tavily.search(query=query, max_results=count)
        print(f"Search successful")
        results = []
        for result in response.get("results", []):
            title = result.get("title", "No Title")
            content = result.get("content", "No Content")
            url = result.get("url", "")
            results.append(f"Title: {title}\nURL: {url}\nContent: {content}\n---")
        
        return "\n".join(results) or "No results found."
    except Exception as e:
        print(f"Search error: {e}")
        return f"Error: {str(e)}"

# FastAPI models
class SearchRequest(BaseModel):
    query: str
    count: int = 3

class SearchResponse(BaseModel):
    results: str

# Expose FastMCP tool via FastAPI REST endpoint
@app.get("/")
def root():
    return {"status": "ok", "service": "Fact Checker MCP Server", "framework": "FastMCP + FastAPI"}

@app.post("/search", response_model=SearchResponse)
def search_endpoint(request: SearchRequest):
    """REST endpoint that calls the FastMCP tool"""
    try:
        # Call the FastMCP tool directly
        result = search(request.query, request.count)
        return SearchResponse(results=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting Hybrid FastMCP + FastAPI server on 0.0.0.0:7860...")
    uvicorn.run(app, host="0.0.0.0", port=7860)
