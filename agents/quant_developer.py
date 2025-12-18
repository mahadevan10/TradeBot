from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.python import PythonTools 
from dotenv import load_dotenv
load_dotenv()

from tools.options_data_tool import get_options_data

# --- The Quant Developer Agent ---
quant_developer = Agent(
    name="Quant Developer",
    role="Computational Finance Engineer",
    model=OpenAIChat(id="gpt-4o"),
    tools=[get_options_data, PythonTools()], 
    instructions=[
        "You are a Senior Quant Developer.",
        
        "**PHASE 1: FETCH DATA**",
        "1. Do NOT write Python code to download data. Use your tool `get_options_data(symbol)` instead.",
        "2. This tool guarantees you get the Valid Strikes and Correct Expiry (Weekly vs Monthly).",
        "3. Read the tool's output carefully to find the 'Selected Chain' and 'ATM Strikes'.",
        
        "**PHASE 2: CALCULATE PAYOFF**",
        "1. Once you have the numbers from Phase 1, use `PythonTools` to calculate the specific trade details.",
        "2. Write a simple script to calculate Max Profit, Max Loss, and Breakevens using the strike/premium you found.",
        "3. Example Script Logic:",
        "   `call_premium = 3.50; strike = 272.5; breakeven = strike + premium; print(breakeven)`",
        
        "**PHASE 3: REPORT**",
        "1. Output the final trade ticket using the EXACT date and strike from Phase 1."
    ]
)
