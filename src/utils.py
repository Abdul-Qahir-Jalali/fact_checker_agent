from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY not found in environment variables.")
    if not os.getenv("MCP_SERVER_URL"):
        raise ValueError("MCP_SERVER_URL not found. Please set it in .env (e.g., http://localhost:8000/sse)")
