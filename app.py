# app.py - The visual interface of our stock agent

import streamlit as st
import plotly.graph_objects as go
from agent import analyze_stock
from tools import get_stock_summary, get_stock_data, get_stock_by_country
from config import EXCHANGE_MAP, STOCK_SETTINGS

# ── PAGE CONFIGURATION ──
st.set_page_config(
    page_title="Stock Analysis Agent",
    page_icon="📈",
    layout="wide"
)

# ── MAIN TITLE ──
st.title("📈 Stock Analysis Agent")
st.subheader("Powered by Gemini AI")

# ── INITIALIZE SESSION STATE ──
if "matches" not in st.session_state:
    st.session_state.matches = []
if "symbol" not in st.session_state:
    st.session_state.symbol = None

# ── COUNTRY DROPDOWN ──
country = st.selectbox("Select Country 🌍", EXCHANGE_MAP.keys())

# ── SEARCH BOX ──
user_input = st.text_input("Enter Company Name 🔍",
             placeholder="e.g. Tata Motors, Reliance, Apple")

# ── SEARCH BUTTON ──
search_button = st.button("Search Stock 🔍")

# ── MAIN LOGIC ──
if search_button and user_input:
    st.session_state.matches = get_stock_by_country(user_input, country)
    st.session_state.symbol = None

if len(st.session_state.matches) == 0 and search_button:
    st.error("No stocks found! Try different name or country.")

elif len(st.session_state.matches) == 1:
    st.session_state.symbol = st.session_state.matches[0]["symbol"]

elif len(st.session_state.matches) > 1:
    options = [m["symbol"] for m in st.session_state.matches]
    st.session_state.symbol = st.selectbox(
        "Multiple stocks found! Select one 👇",
        options=options
    )

# ── ANALYZE BUTTON ──
if st.session_state.symbol:
    analyze_button = st.button("Analyze Stock 🚀")

    if analyze_button:
        with st.spinner("Fetching stock data..."):
            stock_data = get_stock_summary(st.session_state.symbol)
            price_history = get_stock_data(st.session_state.symbol)

        # ── SECTION 1: Company Header ──
        st.header(f"{stock_data['company_name']}")
        st.caption(f"Sector: {stock_data['sector']} | Industry: {stock_data['industry']}")

        # ── SECTION 2: Key Metrics Cards ──
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Current Price", f"₹{stock_data['current_price']}")
        with col2:
            st.metric("52 Week High", f"₹{stock_data['52_week_high']}")
        with col3:
            st.metric("52 Week Low", f"₹{stock_data['52_week_low']}")
        with col4:
            st.metric("PE Ratio", stock_data['pe_ratio'])

        # ── SECTION 2B: Fundamental Metrics ──
        st.subheader("📊 Fundamental Metrics")
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric("PEG Ratio", stock_data['peg_ratio'])
        with col6:
            st.metric("ROE", stock_data['roe'])
        with col7:
            st.metric("Debt/Equity", stock_data['debt_to_equity'])
        with col8:
            st.metric("EPS", stock_data['eps'])

        # ── SECTION 3: Price History Chart ──
        st.subheader("📈 Price History (5 Years)")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=price_history.index,
            y=price_history['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#00C853', width=2)
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            hovermode="x unified",
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── SECTION 4: AI Analysis ──
        st.subheader("🤖 AI Analysis")
        with st.spinner("Gemini is analyzing..."):
            analysis = analyze_stock(st.session_state.symbol)
        st.markdown(analysis)