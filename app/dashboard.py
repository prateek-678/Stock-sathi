import streamlit as st
import pandas as pd
import sys
import os

# Add parent path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.fetch_data import fetch_stock_data
from scripts.plot_graphs import plot_stock_price
from scripts.alert import check_price_alert

# Page setup
st.set_page_config(
    page_title="📈 Stock Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- MASSIVE UI Zoom with High Contrast -------------------
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-size: 20px !important;
            color: #F4F4F4 !important;
        }
        h1, h2, h3 {
            font-weight: 800;
            font-size: 32px !important;
        }
        .stButton button, .stDownloadButton button {
            font-size: 18px !important;
            padding: 0.5rem 1.2rem;
            border-radius: 10px;
        }
        .stTextInput input, .stSelectbox div div div, .stSlider span {
            font-size: 18px !important;
        }

        .metric-box {
            padding: 1rem 1.2rem;
            border-radius: 14px;
            font-weight: 700;
            margin: 1rem 0.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            min-width: 200px;
        }

        .symbol-card { background: #1E3A8A; color: #E0F2FE; }
        .price-card  { background: #166534; color: #D1FAE5; }
        .time-card   { background: #78350F; color: #FFEDD5; }

        .block-title {
            margin-top: 2rem;
            font-size: 28px;
            font-weight: 800;
            color: #FACC15;
        }
    </style>
""", unsafe_allow_html=True)


# ------------------- Sidebar -------------------
st.sidebar.markdown("## ⚙️ Settings")

# Stock symbol selection
COMMON_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "Other (Specify below)"]
selected_option = st.sidebar.selectbox("🔍 Stock Symbol", COMMON_SYMBOLS, index=0)

symbol = ""
if selected_option == "Other (Specify below)":
    custom_symbol = st.sidebar.text_input("Enter Custom Stock Symbol", value="SPY").upper()
    if custom_symbol: # Ensure custom symbol is not empty
        symbol = custom_symbol
    else: # If custom is selected but field is empty, maybe default to first common or show error
        st.sidebar.warning("Please enter a custom symbol or select one from the list.")
        symbol = None # Or a default like "AAPL"
else:
    symbol = selected_option

interval = st.sidebar.selectbox("🕒 Interval", ["1m", "5m", "15m", "1h", "1d"], index=0) # Matched to yfinance intervals
period = st.sidebar.selectbox("📅 Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"], index=0) # Matched to yfinance periods
threshold = st.sidebar.slider("🚨 Alert Threshold (%)", 1, 20, 5) # Increased threshold range
enable_real_time = st.sidebar.checkbox("🚀 Enable Real-Time Updates", value=True)
refresh_interval_seconds = 0
if enable_real_time:
    if interval == "1m":
        refresh_interval_seconds = st.sidebar.select_slider(
            "⏱️ Refresh Interval (seconds)",
            options=[10, 20, 30, 60], # More frequent for 1m data
            value=30
        )
    else:
        refresh_interval_seconds = st.sidebar.select_slider(
            "⏱️ Refresh Interval (seconds)",
            options=[60, 120, 300, 600], # Less frequent for larger intervals
            value=120
        )


# Placeholder for data to persist across reruns if needed for comparison
if 'previous_data' not in st.session_state:
    st.session_state.previous_data = pd.DataFrame()

# ------------------- Header -------------------
st.title("📊 Real-Time Stock Analysis Dashboard")
st.markdown("Get **massively zoomed-in**, high-contrast updates on live stock prices and alerts.")

# Main content area
if symbol:
    # Fetch data: pass the real_time flag
    data = fetch_stock_data(symbol, interval, period, real_time=enable_real_time)

    if not data.empty:
        # Always use the latest available price from the fetched data
        last_price = data['Close'].iloc[-1]
        prev_price = data['Close'].iloc[-2] if len(data) > 1 else last_price
        price_change = last_price - prev_price
        price_change_pct = (price_change / prev_price * 100) if prev_price else 0

        # ------------------- KPI Metrics -------------------
        st.markdown("### 🔎 Summary")
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
            <div class="metric-box symbol-card">
                Symbol<br><span style='font-size:48px'>{symbol.upper()}</span>
            </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
            <div class="metric-box price-card">
                Last Price<br><span style='font-size:48px'>${last_price:.2f}</span><br>
                <span style="color:{'green' if price_change >= 0 else 'red'}; font-size:28px;">
                    {price_change:+.2f} ({price_change_pct:+.2f}%)
                </span>
            </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
            <div class="metric-box time-card">
                Interval / Period<br><span style='font-size:44px'>{interval} / {period}</span>
            </div>
        """, unsafe_allow_html=True)

        # ------------------- Data Table -------------------
        st.markdown("### 🧾 Stock Data (Latest)")
        st.dataframe(data.tail(), height=300, use_container_width=True)

        # ------------------- Price Chart -------------------
        st.markdown("### 📈 Trend Chart")
        fig = plot_stock_price(data, f"{symbol.upper()} Price")
        st.plotly_chart(fig, use_container_width=True)

        # ------------------- Alert Message -------------------
        st.markdown("### 🚨 Alert")
        alert_msg = check_price_alert(data, threshold)
        if "No alert" in alert_msg:
            st.success(alert_msg)
        else:
            st.error(alert_msg)

        # ------------------- Download CSV -------------------
        csv = data.to_csv(index=False).encode()
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"{symbol}_data.csv",
            mime="text/csv"
        )

    else:
        st.warning("⚠️ No data found for this symbol. Try another.")
else:
    st.info("👈 Enter a stock symbol in the sidebar to begin.")

# Auto-refresh mechanism
if enable_real_time and refresh_interval_seconds > 0:
    # Use Streamlit's experimental functionality for auto-refresh
    st.experimental_set_query_params(refresh="true")
    st.rerun()

