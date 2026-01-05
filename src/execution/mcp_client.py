"""
Simple HTTP client for FastAPI endpoint
"""
import httpx
import os

class TavilySearchClient:
    def __init__(self):
        self.server_url = os.getenv("MCP_SERVER_URL")
        
        if not self.server_url:
            raise ValueError("MCP_SERVER_URL is not set")
        
        # Remove /sse suffix if present
        self.server_url = self.server_url.replace("/sse", "").rstrip("/")
        print(f"Search client initialized. Server: {self.server_url}")
    
    async def search(self, query: str, count: int = 3) -> str:
        """Execute a search using the HTTP API"""
        url = f"{self.server_url}/search"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url,
                    json={"query": query, "count": count}
                )
                response.raise_for_status()
                data = response.json()
                
                # Truncate to save tokens
                result = data.get("results", "No results")
                if len(result) > 1500:
                    result = result[:1500] + "..."
                    
                return result
            except httpx.HTTPStatusError as e:
                return f"HTTP Error {e.response.status_code}: {e.response.text}"
            except Exception as e:
                return f"Connection Error: {str(e)}"
