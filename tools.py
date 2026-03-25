# tools.py - eyes and ears of our agent 

import yfinance as yf
import requests
from config import NEWS_API_KEY, STOCK_SETTINGS
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
        "symbol": symbol,                                                                 # Stock symbol e.g. RELIANCE.NS
        "company_name": info.get("longName", info.get("shortName", symbol)),              # Full company name
        "sector": info.get("sector", "N/A"),                                              # e.g. Technology, Finance
        "industry": info.get("industry", "N/A"),                                          # e.g. Software, Banking
        "current_price": info.get("currentPrice", "N/A"),                                 # Today's price
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),                              # Highest price in 1 year
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),                                # Lowest price in 1 year
        "market_cap": info.get("marketCap", "N/A"),                                       # Total company value
        "pe_ratio": info.get("trailingPE", "N/A"),                                        # Price to Earnings ratio
        "description": info.get("longBusinessSummary", "N/A"),                            # What the company does
        "peg_ratio": info.get("pegRatio", "N/A"),                                         # growth adjusted PE ratio
        "roe": info.get("returnOnEquity", "N/A"),                                         # How eficiently company uses equity
        "debt_to_equity": info.get("debtToEquity", "N/A"),                                # How much debt vs equity
        "eps": info.get("trailingEps", "N/A")                                             # Earnings per share
    }

def get_stock_data(symbol, period=STOCK_SETTINGS["default_period"]):
    
    # Look up correct interval for this period
    interval = STOCK_SETTINGS["period_interval_map"].get(period, "1wk")
    # Print message so we know function is running
    print(f"Fetching price history for {symbol}...")
    
    # Create stock object
    stock = yf.Ticker(symbol)
    
    # Fetch historical price data using our settings
    history = stock.history(
        period=period,
        interval=interval
    )
    
    # Return the historical data
    return history

def get_stock_news(query):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("articles", [])