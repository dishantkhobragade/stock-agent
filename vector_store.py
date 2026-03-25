import chromadb
from config import STOCK_SETTINGS

#Create local ChromaDB client 
client = chromadb.PersistentClient(path="./stock_memory")

#Create collection (like a table in normal database)
collection = client.get_or_create_collection(name="stock_data")

def save_stock_analysis(symbol, stock_data):
    document = f"Company: {stock_data['company_name']}, Sector: {stock_data['sector']}, PE Ratio: {stock_data['pe_ratio']}, ROE: {stock_data['roe']}, Debt to equity: {stock_data['debt_to_equity']}, EPS: {stock_data['eps']}"
    collection.upsert(
        documents=[document],
        ids=[symbol]
    )

def get_similar_stocks(query, n_results=STOCK_SETTINGS["vector_search_results"]):
    result = collection.query(
        query_texts = [query],
        n_results = n_results
    )
    return result