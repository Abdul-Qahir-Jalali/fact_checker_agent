from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from src.orchestration.state import AgentState
from langchain_core.output_parsers import JsonOutputParser
from typing import List

def analyze_directive(state: AgentState):
    """
    Analyzes the user statement and generates search queries.
    """
    print(f"--- ANALYZING STATEMENT: {state['statement']} ---")
    
    # Using 8b model for efficiency
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a backend data processor. 
Your goal is to identify the core claims in a user's statement and generate specific search queries to verify them.
Output ONLY a raw JSON object with keys 'claims' (list of strings) and 'search_queries' (list of strings).
Do NOT output markdown code blocks.
Do NOT output any conversational text or preamble.
Example: {{"claims": ["claim1"], "search_queries": ["query1"]}}"""),
        ("user", "Analyze this statement: {statement}")
    ])
    
    chain = prompt | llm | JsonOutputParser()
    
    result = chain.invoke({"statement": state["statement"]})
    
    return {
        "claims": result.get("claims", []),
        "search_queries": result.get("search_queries", [])
    }
