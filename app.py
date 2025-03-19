import streamlit as st
import pandas as pd
import datetime
from alice_client import initialize_alice
from stock_analysis import get_stocks_3_to_5_percent_up, get_stocks_3_to_5_percent_down
from stock_lists import STOCK_LISTS

st.set_page_config(page_title="Stock Screener", layout="wide")

# Store credentials securely in session state
if "user_id" not in st.session_state or "api_key" not in st.session_state:
    st.session_state["user_id"] = None
    st.session_state["api_key"] = None
    st.session_state["login_time"] = None  # Track login time

# User input for AliceBlue API credentials
if st.session_state["user_id"] is None or st.session_state["api_key"] is None:
    st.title("Login to AliceBlue API")
    user_id = st.text_input("Enter User ID", type="password")  # Hide input
    api_key = st.text_input("Enter API Key", type="password")  # Hide input

    if st.button("Login"):
        st.session_state["user_id"] = user_id
        st.session_state["api_key"] = api_key
        st.session_state["login_time"] = datetime.date.today()  # Save login date
        st.rerun()  # Refresh to hide credentials

# Auto-remove credentials at midnight
if st.session_state["login_time"] and st.session_state["login_time"] != datetime.date.today():
    st.session_state["user_id"] = None
    st.session_state["api_key"] = None
    st.session_state["login_time"] = None
    st.rerun()  # Refresh the app

# Initialize AliceBlue API if logged in
if st.session_state["user_id"] and st.session_state["api_key"]:
    try:
        alice = initialize_alice(st.session_state["user_id"], st.session_state["api_key"])
    except Exception as e:
        st.error(f"Failed to initialize AliceBlue API: {e}")
        alice = None
else:
    st.stop()  # Stop execution until user logs in

@st.cache_data(ttl=300)
def fetch_stocks(tokens):
    try:
        if not alice:
            raise Exception("AliceBlue API is not initialized.")
        up_stocks = get_stocks_3_to_5_percent_up(alice, tokens)
        down_stocks = get_stocks_3_to_5_percent_down(alice, tokens)
        return up_stocks, down_stocks
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return [], []

def clean_data(data):
    if not data or not isinstance(data, list):
        return pd.DataFrame(columns=["Name", "Token", "Close", "Change (%)"])
    try:
        df = pd.DataFrame(data)
        df["Close"] = df["Close"].astype(float).round(2)
        df["Change (%)"] = df["Change (%)"].astype(float).round(2)
        return df
    except Exception as e:
        st.error(f"Error processing stock data: {e}")
        return pd.DataFrame(columns=["Name", "Token", "Close", "Change (%)"])

def safe_display(df, title):
    if df.empty:
        st.warning(f"No stocks found for {title}")
    else:
        st.markdown(f"## {title}")
        st.dataframe(df)

st.title("Stock Screener")

selected_list = st.selectbox("Select Stock List:", list(STOCK_LISTS.keys()))
strategy = st.selectbox("Select Strategy:", ["Bullish Stocks", "Bearish Stocks"])

if st.button("Start Screening"):
    tokens = STOCK_LISTS.get(selected_list, [])
    if not tokens:
        st.warning(f"No stocks found for {selected_list}.")
    else:
        stocks_up, stocks_down = fetch_stocks(tokens)
        df = clean_data(stocks_up if strategy == "Bullish Stocks" else stocks_down)
        search = st.text_input("Search Stocks:").upper()
        if search:
            df = df[df["Name"].str.contains(search, na=False, regex=False)]
        safe_display(df, strategy)
