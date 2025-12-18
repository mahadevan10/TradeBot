from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from tools.technical_analysis_tool import get_technical_indicators
from tools.options_data_tool import get_options_data

from dotenv import load_dotenv

load_dotenv()

# 1. The Technical Analyst Agent
technical_agent = Agent(
    name="Technical Analyst",
    role="Analyze price trends and momentum.",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[get_technical_indicators],
    instructions=["Use technical indicators to determine if the trend is Bullish or Bearish."]
)

# 2. The Options Specialist Agent 
quant_agent = Agent(
    name="Quant Specialist",
    role="Analyze volatility and option pricing.",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[get_options_data],
    instructions=["Analyze Implied Volatility (IV) to recommend Credit vs Debit spreads."]
)

# 3. The news sentiment analysis Agent
sentiment_agent = Agent(
    name="News Analyst",
    role="News and Volatility Catalyst Scanner",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools(fixed_max_results=5)],
    instructions=[
        "1. Search for the latest news for the given ticker.",
        "2. CRITICAL: distinct between 'Sentiment' and 'Events'.",
        "   - If there is an Earnings Call, FDA Approval, or Product Launch in < 7 days: Flag Risk as 'HIGH_VOLATILITY_EVENT'.",
        "   - If there is a scandal, lawsuit, or crash: Flag Risk as 'NEGATIVE_CATALYST'.",
        "3. If no major events, determine if sentiment is Bullish, Bearish, or Neutral.",
        "4. Output a concise summary of the top 3 drivers."
    ],
)