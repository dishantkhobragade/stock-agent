# app.py - The visual interface of our stock agent

import streamlit as st
import plotly.graph_objects as go
from agent import analyze_stock, compare_stocks, rag_analysis
from tools import get_stock_summary, get_stock_data, get_stock_by_country, get_stock_news
from config import EXCHANGE_MAP, STOCK_SETTINGS, NEWS_API_KEY
from vector_store import save_stock_analysis, get_similar_stocks


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
if "stock_data" not in st.session_state:
    st.session_state.stock_data = None
if "price_history" not in st.session_state:
    st.session_state.price_history = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "period" not in st.session_state:
    st.session_state.period = "5y"
    


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
                st.session_state.stock_data = get_stock_summary(st.session_state.symbol1)
                save_stock_analysis(st.session_state.symbol1, st.session_state.stock_data)
                st.session_state.price_history = get_stock_data(st.session_state.symbol1, period)
                st.session_state.analysis = analyze_stock(st.session_state.symbol1)

    if st.session_state.stock_data:
        # ── SECTION 1: Company Header ──
        st.header(f"{st.session_state.stock_data['company_name']}")
        st.caption(f"Sector: {st.session_state.stock_data['sector']} | Industry: {st.session_state.stock_data['industry']}")

        # ── SECTION 2: Key Metrics Cards ──
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Current Price", f"₹{st.session_state.stock_data['current_price']}")
        with col2:
            st.metric("52 Week High", f"₹{st.session_state.stock_data['52_week_high']}")
        with col3:
            st.metric("52 Week Low", f"₹{st.session_state.stock_data['52_week_low']}")
        with col4:
            st.metric("PE Ratio", st.session_state.stock_data['pe_ratio'])

        # ── SECTION 2B: Fundamental Metrics ──
        st.subheader("📊 Fundamental Metrics")
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric("PEG Ratio", st.session_state.stock_data['peg_ratio'])
        with col6:
            st.metric("ROE", st.session_state.stock_data['roe'])
        with col7:
            st.metric("Debt/Equity", st.session_state.stock_data['debt_to_equity'])
        with col8:
            st.metric("EPS", st.session_state.stock_data['eps'])

        # ── SECTION 3: Price History Chart ──
        st.subheader(f"📈 Price History | Period: {st.session_state.period}")

        if st.session_state.price_history is not None:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=st.session_state.price_history.index,
                y=st.session_state.price_history['Close'],
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

        analysis_type = st.radio(
            "Select Analysis Type",
            ["📊 Stock Analysis", "🎯 RAG Analysis (BUY/SELL/HOLD)"]
        )
        if analysis_type == "📊 Stock Analysis":
            # ── SECTION 4: AI Analysis ──
            st.subheader("🤖 AI Analysis")
            with st.spinner("Gemini is analyzing..."):
                analysis = analyze_stock(st.session_state.symbol1)
            st.markdown(analysis)
        elif analysis_type == "🎯 RAG Analysis (BUY/SELL/HOLD)":
            # ── SECTION 5: RAG Analysis ──
            st.subheader("🎯 RAG Analysis")
            rag_button = st.button("Get BUY/SELL/HOLD 🎯")

            if rag_button:
                with st.spinner("RAG analyzing..."):
                    st.session_state.rag_result = rag_analysis(st.session_state.symbol1)

            if st.session_state.rag_result:
                st.markdown(st.session_state.rag_result)

with tab2:
    
    col1, col2 = st.columns([2,1])

    with col1:

        st.header("Compare Two Stocks ⚖️")
        s1_col1, s2_col2 = st.columns(2)

        with s1_col1:

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
        
        with s2_col2:

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

        f1_col1, f2_col2, f3_col3 = st.columns(3)

        with f1_col1:
            st.write("Sector")
            st.write("Industry")
            st.write("Current Price")
            st.write("PE Ratio")
            st.write("ROE")
            st.write("Debt/Equity")
            st.write("EPS")
        with f2_col2:
            if st.session_state.symbol1:
                stock_data = get_stock_summary(st.session_state.symbol1)
                st.write(stock_data['sector'])
                st.write(stock_data['industry'])
                st.write(f"₹{stock_data['current_price']}")
                st.write(f"{stock_data['pe_ratio']}")
                st.write(f"{stock_data['roe']}")
                st.write(f"{stock_data['debt_to_equity']}")
                st.write(f"{stock_data['eps']}")
        with f3_col3:
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

    with col2:
        if not (st.session_state.symbol1 or st.session_state.symbol2):
            st.info("Select a stock to view related news")
        else:
            companies = []

            if st.session_state.symbol1:
                s1 = get_stock_summary(st.session_state.symbol1)
                companies.append(s1["company_name"])

            if st.session_state.symbol2:
                s2 = get_stock_summary(st.session_state.symbol2)
                companies.append(s2["company_name"])

            # Combine company names for better search
            search_query = " OR ".join(companies)

            with st.spinner("Fetching latest news..."):
                news_articles = get_stock_news(search_query)

            if not news_articles:
                st.warning("No recent news found.")
            else:
                for article in news_articles:
                    st.markdown(f"### {article['title']}")
                    st.caption(
                        f"{article['source']['name']} | "
                        f"{article['publishedAt'][:10]}"
                    )
                    if article.get("description"):
                        st.write(article["description"])

                    if article.get("url"):
                        st.markdown(f"[Read more →]({article['url']})")

                    st.divider()