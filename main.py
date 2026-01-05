import asyncio
import sys
from src.utils import load_env
from src.orchestration.graph import create_graph

async def main():
    try:
        load_env()
    except Exception as e:
        print(f"Configuration Error: {e}")
        return

    print("Fact Checker Agent Initialized (DO Framework)")
    
    while True:
        user_input = input("\nEnter a statement to verify (or 'q' to quit): ")
        if user_input.lower() in ["q", "quit"]:
            break
            
        print(f"\nProcessing: {user_input}...\n")
        
        graph = create_graph()
        
        initial_state = {"statement": user_input}
        
        try:
            result = await graph.ainvoke(initial_state)
            
            print("\n" + "="*50)
            print(f"VERDICT: {result['verdict']}")
            print("="*50)
            print(f"\nReasoning:\n{result['verification_reasoning']}")
            print("\n" + "="*50)
            
        except Exception as e:
            print(f"An error occurred during execution: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
