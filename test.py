import yfinance as yf

result = yf.Search("tata steel")
quotes = result.quotes

for quote in quotes:
    print(quote.get("symbol"), quote.get("exchange"))