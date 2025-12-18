from agno.agent import Agent
from agno.team import Team 
from agno.models.openai import OpenAIChat

from dotenv import load_dotenv

load_dotenv()
    

# The Synthesizer
# The Manager does NOT have tools or team members. It just has a big brain.
portfolio_manager = Agent(
    name="Portfolio Manager",
    role="Head Trader",
    model=OpenAIChat(id="gpt-4o"),
    # No members list needed here since we are using the Async 'War Room' approach
    instructions=[
        "You are the Head Trader. You have received reports from your team.",
        "1. ANALYZE the News Report First:",
        "   - **CASE A: HIGH_VOLATILITY_EVENT detected (Earnings/FDA):**",
        "     - IGNORE the Technical Trend (charts break during earnings).",
        "     - IGNORE high IV (it is expected).",
        "     - RECOMMENDATION: 'Long Straddle' (if aggressive) or 'Long Strangle' (if conservative).",
        "     - REASONING: 'Betting on massive price expansion due to upcoming event.'",
        "",
        "   - **CASE B: NEGATIVE_CATALYST detected (Scandal/Lawsuit):**",
        "     - RECOMMENDATION: 'NO TRADE' or 'Protective Put'.",
        "     - REASONING: 'Too much unpredictable downside risk.'",
        "",
        "   - **CASE C: Normal Market (No binary events):**",
        "     - Look at the Technical Report for Trend (Bullish/Bearish).",
        "     - Look at the Quant Report for IV (Cheap vs Expensive).",
        "     - Synthesize a standard strategy (e.g., Bull Call Spread, Iron Condor).",
        "",
        "2. Final Output must be a JSON: {Strategy, Ticker, Action, Risk_Profile, Reasoning}."
    ]
)