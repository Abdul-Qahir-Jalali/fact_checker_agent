from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    """
    Represents the state of the fact-checking agent.
    """
    statement: str
    claims: List[str]
    search_queries: List[str]
    search_results: List[str]
    verdict: str
    verification_reasoning: str
