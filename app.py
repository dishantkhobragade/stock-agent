# app.py - The visual interface of our stock agent

import streamlit as st
import plotly.graph_objects as go
from agent import analyze_stock, compare_stocks
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
if "matches1" not in st.session_state:
    st.session_state.matches1 = []
if "symbol1" not in st.session_state:
    st.session_state.symbol1 = None
if "matches2" not in st.session_state:
    st.session_state.matches2 = []
if "symbol2" not in st.session_state:
    st.session_state.symbol2 = None
    


# ── TAB CONFIGURATION ──

tab1, tab2 = st.tabs(["📈 Stock Analysis Agent","⚖️ Compare Stocks"])

with tab1:

    # ── COUNTRY DROPDOWN ──
    country = st.selectbox("Select Country 🌍", EXCHANGE_MAP.keys())

    # ── SEARCH BOX ──
    user_input = st.text_input("Enter Company Name 🔍",
                placeholder="e.g. Tata Motors, Reliance, Apple")

    # ── SEARCH BUTTON ──
    search_button = st.button("Search Stock 🔍")

    # ── MAIN LOGIC ──
    if search_button and user_input:
        st.session_state.matches1 = get_stock_by_country(user_input, country)
        st.session_state.symbol1 = None

    if len(st.session_state.matches1) == 0 and search_button:
        st.error("No stocks found! Try different name or country.")

    elif len(st.session_state.matches1) == 1:
        st.session_state.symbol1 = st.session_state.matches1[0]["symbol"]

    elif len(st.session_state.matches1) > 1:
        options = [f"{m['shortname']} ({m['symbol']})" for m in st.session_state.matches1]
        
        selected_option = st.selectbox(
            "Multiple stocks found! Select one 👇",
            options=options
        )
        
        # Extract symbol from selected option
        st.session_state.symbol1 = selected_option.split("(")[-1].rstrip(")")

    # ── ANALYZE BUTTON ──
    if st.session_state.symbol1:
        period = st.selectbox("Select Period 📅", STOCK_SETTINGS["valid_periods"], index=4)

        analyze_button = st.button("Analyze Stock 🚀")

        if analyze_button:
            with st.spinner("Fetching stock data..."):
                stock_data = get_stock_summary(st.session_state.symbol1)
                price_history = get_stock_data(st.session_state.symbol1, period)

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
            st.subheader(f"📈 Price History | Period: {period}")

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
                analysis = analyze_stock(st.session_state.symbol1)
            st.markdown(analysis)

with tab2:
    
    col1, col2 = st.columns(2)

    with col1:

        st.header("Stock 1")
    
        # ── COUNTRY DROPDOWN ──
        country = st.selectbox("Select Country 🌍", EXCHANGE_MAP.keys(), key = "country1")

        # ── SEARCH BOX ──
        user_input = st.text_input("Enter Company Name 🔍",
                    placeholder="e.g. Tata Motors, Reliance, Apple", key = "input1")

        # ── SEARCH BUTTON ──
        search_button = st.button("Search Stock 🔍", key="search1")

        # ── MAIN LOGIC ──
        if search_button and user_input:
            st.session_state.matches1 = get_stock_by_country(user_input, country)
            st.session_state.symbol1 = None

        if len(st.session_state.matches1) == 0 and search_button:
            st.error("No stocks found! Try different name or country.")

        elif len(st.session_state.matches1) == 1:
            st.session_state.symbol1 = st.session_state.matches1[0]["symbol"]

        elif len(st.session_state.matches1) > 1:
            options = [f"{m['shortname']} ({m['symbol']})" for m in st.session_state.matches1]
            
            selected_option = st.selectbox(
                "Multiple stocks found! Select one 👇",
                options=options, key="select1"
            )
            
            # Extract symbol from selected option
            st.session_state.symbol1 = selected_option.split("(")[-1].rstrip(")")
    
    with col2:

        st.header("Stock 2")
    
        # ── COUNTRY DROPDOWN ──
        country = st.selectbox("Select Country 🌍", EXCHANGE_MAP.keys(), key = "country2")

        # ── SEARCH BOX ──
        user_input = st.text_input("Enter Company Name 🔍",
                    placeholder="e.g. Tata Motors, Reliance, Apple", key = "input2")

        # ── SEARCH BUTTON ──
        search_button = st.button("Search Stock 🔍", key="search2")

        # ── MAIN LOGIC ──
        if search_button and user_input:
            st.session_state.matches2 = get_stock_by_country(user_input, country)
            st.session_state.symbol2 = None

        if len(st.session_state.matches2) == 0 and search_button:
            st.error("No stocks found! Try different name or country.")

        elif len(st.session_state.matches2) == 1:
            st.session_state.symbol2 = st.session_state.matches2[0]["symbol"]

        elif len(st.session_state.matches2) > 1:
            options = [f"{m['shortname']} ({m['symbol']})" for m in st.session_state.matches2]
            
            selected_option = st.selectbox(
                "Multiple stocks found! Select one 👇",
                options=options, key="select2"
            )
            
            # Extract symbol from selected option
            st.session_state.symbol2 = selected_option.split("(")[-1].rstrip(")")
    
    # ── Fundamentals ──

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("Sector")
        st.write("Industry")
        st.write("Current Price")
        st.write("PE Ratio")
        st.write("ROE")
        st.write("Debt/Equity")
        st.write("EPS")
    with col2:
        if st.session_state.symbol1:
            stock_data = get_stock_summary(st.session_state.symbol1)
            st.write(stock_data['sector'])
            st.write(stock_data['industry'])
            st.write(f"₹{stock_data['current_price']}")
            st.write(f"{stock_data['pe_ratio']}")
            st.write(f"{stock_data['roe']}")
            st.write(f"{stock_data['debt_to_equity']}")
            st.write(f"{stock_data['eps']}")
    with col3:
        if st.session_state.symbol2:
            stock_data = get_stock_summary(st.session_state.symbol2)
            st.write(stock_data['sector'])
            st.write(stock_data['industry'])
            st.write(f"₹{stock_data['current_price']}")
            st.write(f"{stock_data['pe_ratio']}")
            st.write(f"{stock_data['roe']}")
            st.write(f"{stock_data['debt_to_equity']}")
            st.write(f"{stock_data['eps']}")
    
    if st.session_state.symbol1 and st.session_state.symbol2:
        period = st.selectbox("Select Period 📅", STOCK_SETTINGS["valid_periods"], index=4, key="period_compare")
        
        # Fetch data for both stocks
        price_history1 = get_stock_data(st.session_state.symbol1, period)
        price_history2 = get_stock_data(st.session_state.symbol2, period)
        
        # ONE figure, TWO traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=price_history1.index,
            y=price_history1['Close'],
            mode='lines',
            name=st.session_state.symbol1,
            line=dict(color='#00C853', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=price_history2.index,
            y=price_history2['Close'],
            mode='lines',
            name=st.session_state.symbol2,
            line=dict(color='#FF0000', width=2)
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

    # ── COMPARE BUTTON ──
    compare_button = st.button("Compare Stocks ⚖️", key="compare_btn")

    if compare_button:
        with st.spinner("Gemini is comparing..."):
            comparison = compare_stocks(st.session_state.symbol1, st.session_state.symbol2)
        st.markdown(comparison)