import pandas_ta as ta 
import pandas as pd 
import yfinance as yf

def get_technical_indicators(symbol: str) -> str:
    """Calculates RSI and EMA to determine trend direction."""
    try:
        # 1. Download 6 months of data (Needed for EMA-20 warm-up)
        df = yf.download(symbol, period="6mo", interval="1d", progress=False, auto_adjust=True)
        
        # 2. Flatten MultiIndex columns (Fixes the yfinance structure issue)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # 3. Clean initial columns to lowercase (so pandas_ta finds 'close')
        df.columns = [c.lower() for c in df.columns]

        if df.empty:
            return f"No data found for {symbol}"

        # 4. Calculate Indicators
        # Note: pandas_ta adds these as 'RSI_14' and 'EMA_20' (Uppercase)
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        
        # 5. CRITICAL FIX: Lowercase columns AGAIN to catch the new indicators
        df.columns = [c.lower() for c in df.columns]
        
        # 6. Get the latest row
        latest = df.iloc[-1]
        
        # Now these keys will definitely match
        current_close = latest.get('close')
        ema_20 = latest.get('ema_20')
        rsi_14 = latest.get('rsi_14')

        # Debugging Print (Optional: Remove in production)
        # print(f"DEBUG: Close={current_close}, EMA={ema_20}, RSI={rsi_14}")

        if pd.isna(ema_20) or pd.isna(rsi_14):
            return f"Not enough data to calculate indicators for {symbol}"

        trend = "BULLISH" if current_close > ema_20 else "BEARISH"
        
        condition = "NEUTRAL"
        if rsi_14 > 70:
            condition = "OVERBOUGHT"
        elif rsi_14 < 30:
            condition = "OVERSOLD"
        
        return f"Trend: {trend} | RSI: {rsi_14:.2f} ({condition})"

    except Exception as e:
        return f"Error calculating technicals: {str(e)}"
    

