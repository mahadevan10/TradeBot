# TradeBot

A AI agent system built using the **Agno** framework. This project demonstrates the orchestration of multiple LLM agents to recommend options trading strategies with strike selection and profit caluclations with premium value of contract.

---

## 🚀 Features
* **Multi-Agent Workflow:** Orchestrates specialized agents for [e.g., searching news, generating and running code for profit, breakeven, loss,etc and a portfolio manager].
* **Real-time Web Access:** Integrated with tools like yfinance toolkit in Agno for current data.
* **Async excecution:** The agents that dont need each others data run asynchronously decreasing the totol time required for output.
* **Custom Technical Analysis(TA) tool:** The tool calculates rsi(14) and EMA 20 for basic TA, but can be expanded or modified as per the need.

## ⚙️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mahadevan10/TradeBot.git
   cd TradeBot

   # On Windows:
   python -m venv venv
   venv\Scripts\activate

   pip install -r requirements.txt

   configure env variables in .env file
   OPENAI_API_KEY = "yourSecretKey"

2.**Usage:** run main.py

## 🚀 Future Improvements

The following features and enhancements are planned for future releases to increase the sophistication and safety of the trading system:

* **Options Strategy Knowledge Base:** Add a dedicated knowledge base for advanced trading strategies specifically for options.
* **Smart Expiry Selection:** Implement the ability to choose the right expiry contract, which is essential for execution.
* **Advanced Technical Analysis:** Upgrade the TA agent with other indicators beyond just a single EMA and RSI.
* **Specialized Risk Management:** Integrate risk management and money management specialist agents to provide sound trading advices.
* **Strategy Visualization:** Utilize `matplotlib` or `seaborn` for plotting payoff graphs for various strategies.
* **Greeks Integration:** Ensure Option greeks are considered more in decision-making processes.
* **Quant Safety & Guardrails:** Implement a sandbox environment for the Quant developer agent to act as guardrails.
* **Black Swan Protection:** Develop logic to ensure protection against blackswan events is considered.
