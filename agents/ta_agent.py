from agno.agent import Agent
from agno.models.openai import OpenAIChat


from tools.technical_analysis_tool import get_technical_indicators

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


