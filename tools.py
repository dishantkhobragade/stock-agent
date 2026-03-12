# tools.py - eyes and ears of our agent 

import yfinance as yf
from config import STOCK_SETTINGS
from config import EXCHANGE_MAP

def get_stock_by_country(user_input,country):
    user_input = user_input.strip()
    result = yf.Search(user_input)
    quotes = result.quotes
    country_exchanges = EXCHANGE_MAP.get(country, []) 

    matches = []
    for quote in quotes:
        if quote["exchange"] in country_exchanges:
            matches.append(quote)
    return matches

    

def resolve_symbol(user_input):
    user_input = user_input.strip()
    result = yf.Search(user_input)
    quotes = result.quotes
    
    if not quotes:
        return user_input
    
    # Loop through all results
    for quote in quotes:
        # Check if it's an Indian stock
        if quote["exchange"] == "NSI" or quote["exchange"] == "BSE":
            return quote["symbol"]
    
    # No Indian stock found → return first result
    return quotes[0]["symbol"]

def get_stock_summary(symbol):
    # Print a message so we know the function is running
    print(f"Getting summary for {symbol}...")
    
    # Create a stock object for the given symbol (e.g. "RELIANCE.NS")
    stock = yf.Ticker(symbol)
    
    # Fetch all available info about the company
    info = stock.info
    
    # Return a dictionary with the most important details
    # info.get("key", "N/A") means:
    # → try to get this value, if not available return "N/A"
    return {
        "symbol": symbol,                                           # Stock symbol e.g. RELIANCE.NS
        "company_name": info.get("longName", symbol),              # Full company name
        "sector": info.get("sector", "N/A"),                       # e.g. Technology, Finance
        "industry": info.get("industry", "N/A"),                   # e.g. Software, Banking
        "current_price": info.get("currentPrice", "N/A"),          # Today's price
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),       # Highest price in 1 year
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),         # Lowest price in 1 year
        "market_cap": info.get("marketCap", "N/A"),                # Total company value
        "pe_ratio": info.get("trailingPE", "N/A"),                 # Price to Earnings ratio
        "description": info.get("longBusinessSummary", "N/A"),     # What the company does
        "peg_ratio": info.get("pegRatio", "N/A"),                  # growth adjusted PE ratio
        "roe": info.get("returnOnEquity", "N/A"),                  # How eficiently company uses equity
        "debt_to_equity": info.get("debtToEquity", "N/A"),         # How much debt vs equity
        "eps": info.get("trailingEps", "N/A")                      # Earnings per share
    }

def get_stock_data(symbol):
    # Print message so we know function is running
    print(f"Fetching price history for {symbol}...")
    
    # Create stock object
    stock = yf.Ticker(symbol)
    
    # Fetch historical price data using our settings
    history = stock.history(
        period=STOCK_SETTINGS["default_period"],
        interval=STOCK_SETTINGS["default_interval"]
    )
    
    # Return the historical data
    return history