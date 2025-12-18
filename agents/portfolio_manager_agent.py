from agno.agent import Agent
from agno.team import Team 
from agno.models.openai import OpenAIChat

from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field
from typing import List, Union, Literal

class TradeLeg(BaseModel):
    action: str = Field(..., description="BUY or SELL")
    contract_type: str = Field(..., description="CALL or PUT")
    strike_price: float = Field(..., description="The specific strike price (e.g., 150.0)")
    premium: float = Field(..., description="The price of the option leg")

class TradeSignal(BaseModel):
    ticker: str
    signal: str = Field(..., description="BULLISH, BEARISH, NEUTRAL, or NO_TRADE")
    strategy_name: str = Field(..., description="e.g., 'Bull Put Spread', 'Iron Condor'")
    
    # Specific Trade Details (Extracted from Quant Report)
    legs: List[TradeLeg] = Field(..., description="List of option legs to execute")
    max_profit: Union[float, Literal["Unlimited"]] = Field(
        ..., 
        description="Max profit in $. If profit is infinite (e.g. Long Call), strictly return the string 'Unlimited'."
    )
    max_loss: Union[float, Literal["Unlimited"]] = Field(
        ..., 
        description="Max risk in $. If risk is infinite (e.g. Short Straddle), strictly return the string 'Unlimited'."
    )
    risk_reward_ratio: str = Field(..., description="e.g., '1:2.5'")
    
    # Validation & Context
    breakeven_point: str = Field(..., description="Price level description (e.g. 'Above $145.50')")
    conviction_score: int = Field(..., description="0-10 score based on News/Tech alignment")
    reasoning: str = Field(..., description="Final synthesis of why this trade was chosen")
    

# The Manager does NOT have tools or team members. It just has a big brain.
portfolio_manager = Agent(
    name="Portfolio Manager",
    role="Final Gatekeeper & Trade Structurer",
    model=OpenAIChat(id="gpt-4o"),
    
    # Enforce the Strict JSON Output
    output_schema=TradeSignal,
    
    instructions=[
        "You are the Chief Investment Officer (CIO).",
        "You have received a fully engineered trade plan from your Quant Developer, based on News and Technicals.",
        
        "**YOUR RESPONSIBILITIES:**",
        "1. **Validation (The Sanity Check):**",
        "   - Check if the Strategy matches the News Sentiment.",
        "   - *CRITICAL:* If News reported a 'High Risk/Lawsuit' but the Quant coded a Bullish trade -> OVERRIDE signal to 'NO_TRADE'.",
        
        "2. **Extraction (Data Entry):**",
        "   - Read the 'Quant Calculation' report carefully.",
        "   - Extract the EXACT Strikes, Premiums, Max Profit, and Max Loss values printed by the Python script.",
        "   - Do not calculate these yourself; trust the Code's output.",
        
        "3. **Formatting:**",
        "   - Fill out the 'TradeSignal' JSON fields.",
        "   - Calculate 'Risk/Reward Ratio' simply as (Max Profit / Max Loss).",
        "   - For 'conviction_score', give a 10 if News, Tech, and Math all agree. Deduct points for conflicting signals.",
        
        "4. **Final Output:**",
        "   - Return ONLY the structured JSON object."
    ],
    # Markdown is False because we want raw JSON for the Pydantic model
    markdown=False, 
)