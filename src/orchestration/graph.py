from langgraph.graph import StateGraph, END
from src.orchestration.state import AgentState
from src.directives.analysis import analyze_directive
from src.directives.verification import verification_directive
from src.execution.mcp_client import TavilySearchClient
import asyncio

# --- NODE WRAPPERS ---

async def analyze_node(state: AgentState):
    return analyze_directive(state)

async def search_node(state: AgentState):
    print(f"--- PERFORMING SEARCH ---")
    queries = state["search_queries"]
    results = []
    
    # Instantiate client here (or pass it in config)
    client = TavilySearchClient()
    
    # potentially run in parallel
    for query in queries:
        try:
            print(f"Searching for: {query}")
            res = await client.search(query)
            results.append(f"Query: {query}\nResult: {res}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            results.append(f"Query: {query}\nError: {str(e)}")
            
    print(f"DEBUG: Search results count: {len(results)}")
    if results:
        print(f"DEBUG: First result preview: {results[0][:200]}...")
    
    return {"search_results": results}

async def verify_node(state: AgentState):
    return verification_directive(state)

# --- GRAPH DEFINITION ---

def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("search", search_node)
    workflow.add_node("verify", verify_node)
    
    workflow.set_entry_point("analyze")
    
    workflow.add_edge("analyze", "search")
    workflow.add_edge("search", "verify")
    workflow.add_edge("verify", END)
    
    return workflow.compile()
