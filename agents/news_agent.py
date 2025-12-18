from agno.agent import Agent
from agno.models.openai import OpenAIChat

from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
load_dotenv()

sentiment_agent = Agent(
    name="News Analyst",
    role="News and Volatility Catalyst Scanner",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[
        YFinanceTools(
            # ENABLE ONLY NEWS & PRICE:
            # We explicitly list only the tools we want the agent to see.
            # This replaces the old 'company_news=True' style.
            include_tools=[
                "get_company_news", 
                "get_current_stock_price",
                "get_analyst_recommendations"
            ]
        )
    ],
    instructions=[
        "1. Use get_company_news to fetch the latest stories for the given ticker.",
        "2. CRITICAL: Distinguish between 'Sentiment' and 'Events'.",
        "   - If there is an Earnings Call, FDA Approval, or Product Launch in < 7 days: Flag Risk as 'HIGH_VOLATILITY_EVENT'.",
        "   - If there is a scandal, lawsuit, or crash: Flag Risk as 'NEGATIVE_CATALYST'.",
        "3. If no major events, determine if sentiment is Bullish, Bearish, or Neutral.",
        "4. Output a concise summary of the top 3 drivers.",
        "5. Always mention the publication date to ensure the news is fresh."
    ],
    markdown=True,
)

