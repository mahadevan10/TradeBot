import asyncio
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from datetime import datetime

from agents.sub_agents import sentiment_agent, technical_agent 
from agents.portfolio_manager_agent import portfolio_manager
from agents.quant_developer import quant_developer

async def run_smart_trading_floor(ticker: str):
    print(f"⚡ [Phase 1] Gathering Intelligence for {ticker}...")

    # 1. GET CURRENT DATE (Critical for calculating Days to Expiry)
    # We fetch this instantly. It's fast enough that it doesn't need its own async task.
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Date Context: {current_date}")

    # --- PHASE 1: PARALLEL RECONNAISSANCE ---
    # We only run the "eyes" (News & Tech) first.
    news_task = sentiment_agent.arun(f"Today is {current_date}. Check for immediate news/earnings for {ticker}.")
    tech_task = technical_agent.arun(f"Analyze the technical trend for {ticker}.")
    
    # Wait for both to finish
    results = await asyncio.gather(news_task, tech_task)
    news_report = results[0].content
    tech_report = results[1].content
    
    print("✅ Intelligence gathered. Analyzing Strategy...")

    # --- PHASE 2: CONTEXTUAL QUANT EXECUTION ---
    # We construct a prompt that includes the findings from Phase 1.
    # This allows the Quant Developer to be smart: "Oh, RSI is 80? I'll code a Bear Spread."
    
    quant_prompt = f"""
        **CURRENT DATE:** {current_date} (Use this for 'Days to Expiry' calculations).
        
        [NEWS INTEL]: {news_report}
        [TECHNICAL INTEL]: {tech_report}
        
        **YOUR MISSION:**
        1. Decide the SINGLE best option strategy based on the intel above.
        2. **WRITE AND EXECUTE A PYTHON SCRIPT** using `yfinance`:
        - Fetch live option chain.
        - **CRITICAL:** Calculate 'Days to Expiry' = (ExpiryDate - '{current_date}').
        - If Days to Expiry < 7: Code a high-gamma trade (Straddle).
        - If Days to Expiry > 30: Code a theta-safe trade (Spread).
        - Calculate: Strikes, Max Profit, Max Loss.
        - PRINT result: "STRATEGY: [Name] | LEGS: [Details] | PROFIT: [Amount]"
        """

    print(f"⚡ [Phase 3] Quant Developer is engineering the best trade...")
    # This runs sequentially after we know the trend
    quant_response = await quant_developer.arun(quant_prompt)
    
    print("✅ Math execution complete.")

    # --- PHASE 4: FINAL PORTFOLIO MANAGER DECISION ---
    # Now the Manager just needs to package it (using the Pydantic model from previous steps)
    final_prompt = f"""
        Construct the final trade signal based on this completed analysis:
        
        [DATE]: {current_date}
        [NEWS]: {news_report}
        [TECHNICAL]: {tech_report}
        [QUANT CALCULATION]: {quant_response.content}
        """
    
    portfolio_manager.print_response(final_prompt, stream=True)

if __name__ == "__main__":
    asyncio.run(run_smart_trading_floor("NVDA"))