# agent.py - The brain of our stock agent

from google import genai
from config import GEMINI_API_KEY
from tools import get_stock_summary

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