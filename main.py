import asyncio
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from agents.sub_agents import sentiment_agent, technical_agent, quant_agent
from agents.portfolio_manager_agent import portfolio_manager


async def run_trading_floor(ticker: str):
    print(f"⚡ Starting parallel analysis for {ticker}...")

    # 1. Create the prompts
    news_prompt = f"Check for immediate news risks for {ticker}."
    tech_prompt = f"Analyze the technical trend for {ticker}."
    quant_prompt = f"Get options chain and IV analysis for {ticker}."

    # 2. Fire all 3 agents at the exact same time
    # .arun() is the Async version of .run()
    task1 = sentiment_agent.arun(news_prompt)
    task2 = technical_agent.arun(tech_prompt)
    task3 = quant_agent.arun(quant_prompt)

    # 3. Wait for all of them to finish (Async Gather)
    # This takes as long as the SLOWEST agent (e.g., 15s), not the sum of all three.
    results = await asyncio.gather(task1, task2, task3)
    
    # Unpack results
    news_response = results[0].content
    tech_response = results[1].content
    quant_response = results[2].content

    print("✅ All analysts have reported in.")

    # 4. Feed everything to the Manager
    final_prompt = f"""
    Analyze these reports and make a trading decision for {ticker}:
    
    --- [NEWS REPORT] ---
    {news_response}
    
    --- [TECHNICAL REPORT] ---
    {tech_response}
    
    --- [QUANT REPORT] ---
    {quant_response}
    """
    
    # The Manager runs synchronously (blocking) because it's the final step
    portfolio_manager.print_response(final_prompt, stream=True)

# --- STEP 4: Run It ---
if __name__ == "__main__":
    asyncio.run(run_trading_floor("AAPL"))