# agent.py - The brain of our stock agent

from google import genai
from config import GEMINI_API_KEY
from tools import get_stock_summary, get_stock_news
from vector_store import get_similar_stocks

# Connect to Gemini AI using our API key
client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_stock(symbol):
    print(f"Analyzing {symbol}...")
    
    # Step 1 - Fetch real stock data using our tools.py
    stock_data = get_stock_summary(symbol)
    
    # Step 2 - Build a prompt for Gemini AI
    prompt = f"""
    You are an expert stock analyst. Analyze this stock:
    
    Company: {stock_data['company_name']}
    Sector: {stock_data['sector']}
    Current Price: {stock_data['current_price']}
    52 Week High: {stock_data['52_week_high']}
    52 Week Low: {stock_data['52_week_low']}
    PE Ratio: {stock_data['pe_ratio']}
    About: {stock_data['description']}
    
    Please provide:
    1. Overall analysis of this stock
    2. Is it currently cheap or expensive?
    3. Key risks to watch
    4. Your prediction for next 6 months
    """
    
    # Step 3 - Send prompt to Gemini and get analysis
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    # Step 4 - Return Gemini's analysis
    return response.text

# --Stock Analysis for 2 Stocks--

def compare_stocks(symbol1, symbol2):
    print(f"Comparing {symbol1} vs {symbol2}...")
    
    # Fetch data for both stocks
    stock_data1 = get_stock_summary(symbol1)
    stock_data2 = get_stock_summary(symbol2)
    
    prompt = f"""
    You are an expert stock analyst. Compare these two stocks:
    
    Stock 1: {stock_data1['company_name']}
    Sector: {stock_data1['sector']}
    Current Price: {stock_data1['current_price']}
    PE Ratio: {stock_data1['pe_ratio']}
    ROE: {stock_data1['roe']}
    Debt/Equity: {stock_data1['debt_to_equity']}
    EPS: {stock_data1['eps']}
    
    Stock 2: {stock_data2['company_name']}
    Sector: {stock_data2['sector']}
    Current Price: {stock_data2['current_price']}
    PE Ratio: {stock_data2['pe_ratio']}
    ROE: {stock_data2['roe']}
    Debt/Equity: {stock_data2['debt_to_equity']}
    EPS: {stock_data2['eps']}
    
    Please provide:
    1. Overall comparison
    2. Which is cheaper/expensive?
    3. Key risks for both
    4. 6 month prediction for both
    5. Which is better for long term and why?
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text

def rag_analysis(symbol):
    past_data = get_similar_stocks(symbol, n_results=1)
    current_data = get_stock_summary(symbol)
    news = get_stock_news(current_data['company_name'])

    prompt = f"""
    You are an expert stock analyst.

    PAST ANALYSIS FROM MEMORY:
    {past_data}

    CURRENT FUNDAMENTALS:
    Company: {current_data['company_name']}
    PE Ratio: {current_data['pe_ratio']}
    ROE: {current_data['roe']}
    EPS: {current_data['eps']}
    Current Price: {current_data['current_price']}

    LATEST NEWS:
    {news}

    Please provide:
    1. Overall analysis
    2. Is it cheap or expensive?
    3. Key risks
    4. 6 month prediction
    5. BUY / SELL / HOLD recommendation
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


