# Stock Agent - Progress Tracker
By Dishant Khobragade 🚀

## How to Run
1. Activate venv: `.venv\Scripts\activate`
2. Run app: `streamlit run app.py`
3. Open browser and search for any stock!

## Project Structure
- **config.py** → Configuration, settings, exchange map
- **tools.py** → Data fetching functions (yfinance)
- **agent.py** → AI brain (Gemini 2.5-flash)
- **app.py** → Web UI (Streamlit)

---

## ✅ Phase 1 — Core Agent (COMPLETE)
✅ config.py → API key + STOCK_SETTINGS + EXCHANGE_MAP (40+ countries)
✅ tools.py → get_stock_summary(), get_stock_data(), get_stock_by_country()
✅ agent.py → Gemini 2.5-flash analysis
✅ app.py → Streamlit UI
✅ GitHub → Code live online

---

## ⚡ Phase 2 — Better Analysis (IN PROGRESS)
✅ Fundamental ratios in tools.py (PEG, ROE, Debt/Equity, EPS)
✅ Fundamental ratios displayed in app.py
✅ Country dropdown (40+ countries)
✅ Exchange selector (multiple stocks per country)
✅ session_state fixed
✅ Better stock display with shortname + symbol
✅ Symbol extraction from dropdown selection
✅ Period dropdown with smart interval auto-mapping
✅ Interval dropdown removed (clean UI!)
✅ Company name header fixed (longName → shortName fallback)
✅ Dynamic price history title showing selected period
✅ Tabs added → "📈 Stock Analysis" | "⚖️ Compare Stocks"
✅ Compare mode → side by side search (Stock 1 | Stock 2)
✅ Fundamentals comparison table (3 column layout)

⏳ Overlapping price chart in Compare tab
⏳ AI consolidated summary in Compare tab
⏳ Indian news feed

---

## ⏳ Phase 3 — True Agentic AI
⏳ Agent decides what to fetch on its own
⏳ Multi stock comparison automatically
⏳ News + data analysis together
⏳ Memory (remembers past analyses)
⏳ "Which stock should I buy?" → agent decides!

---

## ⏳ Phase 4 — LangChain Integration
→ Build manually first, then LangChain makes sense!

---

## ⏳ Phase 5 — CrewAI Multi-Agent
Agent 1 (Researcher)  → fetches all stock data
Agent 2 (Analyst)     → analyzes fundamentals
Agent 3 (News Reader) → reads latest news
Agent 4 (Advisor)     → gives final recommendation

---

## 🧠 Key Concepts Learned
- Variables, Dictionaries, Functions, Classes
- f-strings, .get(), if/else, for loops
- List comprehension
- session_state → Streamlit memory between reruns
- Separation of concerns → tools.py vs app.py
- Input validation → dropdowns > free text
- String parsing → split("(")[-1].rstrip(")")
- Nested .get() → fallback chaining
- Smart period/interval mapping
- Streamlit tabs, columns, widgets
- Unique keys for duplicate Streamlit widgets
- Dead code removal

---

## 💡 Golden Rules
1. Concepts > Syntax
2. Always activate .venv before running
3. Never let Copilot touch terminal
4. Test don't assume!
5. Single source of truth → config.py
6. Separation of concerns → tools.py = data, app.py = UI
7. Never push config.py to GitHub (API keys!)
8. Kill streamlit → Ctrl+C
9. Dead code → delete it!
10. Wrong symbol = wrong data → always verify!

---

## 🔗 GitHub
https://github.com/dishantkhobragade/stock-agent