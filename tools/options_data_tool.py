import yfinance as yf
import pandas as pd

def get_options_data(symbol: str) -> str:
    """
    Fetches the current price and the TRUE nearest ATM options.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # 1. Reliable Price Fetching
        # 'fast_info' is often faster and more reliable than 'info' in newer yfinance versions
        try:
            price = ticker.fast_info['last_price']
        except:
            price = ticker.info.get('currentPrice', ticker.info.get('regularMarketPrice'))
        
        if not ticker.options:
            return f"No options data found for {symbol}"
        
        # 2. Get Expiration
        expiration = ticker.options[0]
        opt = ticker.option_chain(expiration)
        
        # 3. THE FIX: Define a helper to sort by closeness to price
        def get_atm_strikes(df, current_price, n=5):
            if df.empty: return df
            # Create a copy to avoid SettingWithCopy warnings
            df = df.copy()
            # Calculate absolute distance from current price
            df['distance'] = abs(df['strike'] - current_price)
            # Sort by distance (smallest first) and take top n
            return df.sort_values('distance').head(n).sort_values('strike')

        # 4. Get the true ATM options
        atm_calls = get_atm_strikes(opt.calls, price)
        atm_puts = get_atm_strikes(opt.puts, price)
        
        # 5. Calculate Average IV for the ATM striks (Better indicator than single strike)
        avg_iv_calls = atm_calls['impliedVolatility'].mean()
        avg_iv_puts = atm_puts['impliedVolatility'].mean()
        avg_iv = (avg_iv_calls + avg_iv_puts) / 2

        return f"""
        Stock: {symbol}
        Current Price: ${price:.2f}
        Next Expiry: {expiration}
        Approx ATM IV: {avg_iv:.2%}
        
        --- TOP 5 CLOSEST ATM CALLS ---
        {atm_calls[['strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility']].to_string(index=False)}
        
        --- TOP 5 CLOSEST ATM PUTS ---
        {atm_puts[['strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility']].to_string(index=False)}
        """
    except Exception as e:
        return f"Error fetching data: {str(e)}"