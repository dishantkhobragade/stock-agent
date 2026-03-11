# app.py - The visual interface of our stock agent

import streamlit as st
import plotly.graph_objects as go
from agent import analyze_stock
from tools import get_stock_summary, get_stock_data, resolve_symbol

# ── PAGE CONFIGURATION ──
# This sets up the browser tab title and layout
st.set_page_config(
    page_title="Stock Analysis Agent",
    page_icon="📈",
    layout="wide"
)

# ── MAIN TITLE ──
st.title("📈 Stock Analysis Agent")
st.subheader("Powered by Gemini AI")

# ── SEARCH BOX ──
# User types stock symbol here
symbol = st.text_input(
    "Enter Stock Symbol",
    placeholder="e.g. RELIANCE.NS, TCS.NS, INFY.NS"
)

# ── ANALYZE BUTTON ──
analyze_button = st.button("Analyze Stock 🔍")

# ── MAIN LOGIC ──
# Only runs when user clicks the button
if analyze_button and symbol:
    symbol = resolve_symbol(symbol)  # Convert user input to valid stock symbol

    # Show loading spinner while fetching data
    with st.spinner("Fetching stock data..."):
        stock_data = get_stock_summary(symbol)
        price_history = get_stock_data(symbol)

    # ── SECTION 1: Company Header ──
    st.header(f"{stock_data['company_name']}")
    st.caption(f"Sector: {stock_data['sector']} | Industry: {stock_data['industry']}")

    # ── SECTION 2: Key Metrics Cards ──
    # Creates 4 columns side by side
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Current Price", f"₹{stock_data['current_price']}")

    with col2:
        st.metric("52 Week High", f"₹{stock_data['52_week_high']}")

    with col3:
        st.metric("52 Week Low", f"₹{stock_data['52_week_low']}")

    with col4:
        st.metric("PE Ratio", stock_data['pe_ratio'])

    # ── SECTION 3: Price History Chart ──
    st.subheader("📈 Price History (5 Years)")

    # Create interactive chart using Plotly
    fig = go.Figure()

    # Add price line to chart
    fig.add_trace(go.Scatter(
        x=price_history.index,       # Dates on X axis
        y=price_history['Close'],    # Closing prices on Y axis
        mode='lines',                # Show as a line
        name='Close Price',
        line=dict(color='#00C853', width=2)  # Green line
    ))

    # Style the chart
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode="x unified",        # Show values on hover
        plot_bgcolor='#0E1117',       # Dark background
        paper_bgcolor='#0E1117',
        font=dict(color='white')
    )

    # Display chart in app
    st.plotly_chart(fig, use_container_width=True)

    # ── SECTION 4: AI Analysis ──
    st.subheader("🤖 AI Analysis")

    # Show spinner while Gemini thinks
    with st.spinner("Gemini is analyzing..."):
        analysis = analyze_stock(symbol)

    # Display Gemini's analysis
    st.markdown(analysis)