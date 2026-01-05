from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from src.orchestration.state import AgentState
from langchain_core.output_parsers import JsonOutputParser

def verification_directive(state: AgentState):
    """
    Verifies the claims against the search results.
    """
    print(f"--- VERIFYING CLAIMS ---")
    
    # Using 8b model for efficiency
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict fact-checker. 
Given claims and search results, you MUST provide a clear verdict: VERIFIED, REFUTED, or UNVERIFIED.

VERIFIED: Search results clearly support the claim
REFUTED: Search results clearly contradict the claim OR the claim involves obviously false information
UNVERIFIED: Insufficient information in search results

Output ONLY a raw JSON object.
Do NOT output markdown code blocks.
Do NOT output any conversational text or preamble.

Return ONLY valid JSON with this structure:
{{
    "verdict": "VERIFIED" or "REFUTED" or "UNVERIFIED",
    "reasoning": "Clear explanation citing specific evidence from search results or knowledge"
}}"""),
        ("user", "Original Statement: {statement}\n\nClaims Identified:\n{claims}\n\nSearch Results:\n{search_results}\n\nProvide your fact-check verdict.")
    ])
    
    chain = prompt | llm | JsonOutputParser()
    
    # Format search results as a single string
    search_results_str = "\n\n".join(state["search_results"])
    
    result = chain.invoke({
        "statement": state["statement"],
        "claims": state["claims"],
        "search_results": search_results_str
    })
    
    return {
        "verdict": result.get("verdict", "[UNVERIFIED]"),
        "verification_reasoning": result.get("reasoning", "No reasoning provided.")
    }
