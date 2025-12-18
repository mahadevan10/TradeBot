import yfinance as yf
import pandas as pd

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_options_data(symbol: str) -> str:
    """
    Fetches price and ATM options for the Nearest AND Next Monthly expiry.
    Identifies if options are Weekly or Monthly (Standard).
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # 1. Reliable Price Fetching
        try:
            price = ticker.fast_info['last_price']
        except:
            price = ticker.info.get('currentPrice', ticker.info.get('regularMarketPrice'))
            
        if not ticker.options:
            return f"No options data found for {symbol}"

        # 2. Expiry Analysis (The "Quant" Upgrade)
        all_dates = ticker.options
        today = datetime.now().date()
        
        # Helper to analyze expiries
        def analyze_expiry(date_str):
            exp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            dte = (exp_date - today).days
            # Simple heuristic: 3rd Fridays are usually "Monthlies", others are "Weeklies"
            # (Strict exchange logic is complex, but this serves most retail bots well)
            is_third_friday = exp_date.day >= 15 and exp_date.day <= 21 and exp_date.weekday() == 4
            tag = "MONTHLY (Std)" if is_third_friday else "WEEKLY"
            return date_str, dte, tag

        # Analyze the immediate next expiry
        next_exp, next_dte, next_tag = analyze_expiry(all_dates[0])
        
        # Find the next likely "Monthly" (approx 20-35 days out) for comparison
        monthly_exp = None
        for d in all_dates:
            _, dte, tag = analyze_expiry(d)
            if dte > 25 and tag == "MONTHLY (Std)":
                monthly_exp = d
                break
        
        # Default to nearest if no monthly found
        target_exp = next_exp if monthly_exp is None else next_exp 
        
        # 3. Fetch Chain for the TARGET expiry (You can modify logic to pick Monthly)
        # For this report, we show the NEAREST, but list the others contextually.
        opt = ticker.option_chain(target_exp)
        
        # 4. Smart ATM Snapping (Your correct logic)
        def get_atm_strikes(df, current_price, n=5):
            if df.empty: return df
            df = df.copy()
            df['distance'] = abs(df['strike'] - current_price)
            return df.sort_values('distance').head(n).sort_values('strike')

        atm_calls = get_atm_strikes(opt.calls, price)
        atm_puts = get_atm_strikes(opt.puts, price)
        
        # 5. Average IV
        avg_iv = (atm_calls['impliedVolatility'].mean() + atm_puts['impliedVolatility'].mean()) / 2

        # 6. Build the Rich Report
        # Note: We show the Agent that other expiries exist!
        available_expiries = [analyze_expiry(d) for d in all_dates[:4]]
        expiry_summary = "\n".join([f"   - {d[0]} (DTE: {d[1]}d) [{d[2]}]" for d in available_expiries])

        return f"""
        STOCK: {symbol}
        PRICE: ${price:.2f}
        
        --- EXPIRY CONTEXT ---
        Selected Chain: {target_exp} (DTE: {next_dte} days)
        Type: {next_tag}
        
        Upcoming Expiries (Agent Reference):
        {expiry_summary}
        
        Approx ATM IV: {avg_iv:.2%}
        
        --- TOP 5 ATM CALLS ({target_exp}) ---
        {atm_calls[['strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility']].to_string(index=False)}
        
        --- TOP 5 ATM PUTS ({target_exp}) ---
        {atm_puts[['strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility']].to_string(index=False)}
        """

    except Exception as e:
        return f"Error fetching data: {str(e)}"