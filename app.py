import streamlit as st
import pandas as pd
from alice_client import initialize_alice
from stock_analysis import get_stocks_3_to_5_percent_up, get_stocks_3_to_5_percent_down
from stock_lists import STOCK_LISTS

st.set_page_config(page_title="Stock Screener", layout="wide")

try:
    alice = initialize_alice()
except Exception as e:
    st.error(f"Failed to initialize AliceBlue API: {e}")
    alice = None

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
