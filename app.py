import streamlit as st
import pandas as pd
from alice_client import initialize_alice
from stock_analysis import get_stocks_3_to_5_percent_up, get_stocks_3_to_5_percent_down
from stock_lists import STOCK_LISTS

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Stock Screener", layout="wide")

# Initialize AliceBlue API
alice = initialize_alice()

# Browser compatibility warning
st.info("ℹ️ For best experience, use the latest Chrome/Firefox/Safari. Some features may not work on outdated browsers.")

@st.cache_data(ttl=300)  # Cache results for 5 minutes
def fetch_stocks(tokens):
    """Fetch stock data for selected tokens."""
    if not tokens:
        return [], []
    
    try:
        return get_stocks_3_to_5_percent_up(alice, tokens), get_stocks_3_to_5_percent_down(alice, tokens)
    except Exception as e:
        st.error(f"⚠️ Error fetching stock data: {e}")
        return [], []

def clean_dataframe(data):
    """Convert raw stock data into a clean DataFrame."""
    if not data:
        return pd.DataFrame(columns=["Name", "Token", "Close", "Change (%)"])
    
    df = pd.DataFrame(data, columns=["Name", "Token", "Close", "Change (%)"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df["Change (%)"] = pd.to_numeric(df["Change (%)"], errors="coerce")
    return df.dropna().reset_index(drop=True)

# App title
st.title("📈 Stock Screener - Daily Movers")

# Selection Widgets
selected_list = st.selectbox("📋 Select Stock List:", list(STOCK_LISTS.keys()))
strategy = st.radio("🎯 Select Strategy:", ["📈 Bullish Stocks", "📉 Bearish Stocks"])

# **Fetch Data on Button Click**
if st.button("🚀 Start Screening"):
    tokens = STOCK_LISTS[selected_list]

    if not tokens:
        st.warning(f"No tokens available for **{selected_list}**.")
    else:
        with st.spinner("Fetching stocks..."):
            stocks_up_3_to_5, stocks_down_3_to_5 = fetch_stocks(tokens)

        # **Bullish Stocks**
        if strategy == "📈 Bullish Stocks":
            df_up = clean_dataframe(stocks_up_3_to_5)
            if df_up.empty:
                st.warning(f"No bullish stocks in **{selected_list}** met the criteria.")
            else:
                search_up = st.text_input("🔍 Search Bullish Stock:").upper()
                if search_up:
                    df_up = df_up[df_up["Name"].str.contains(search_up, na=False, regex=False)]
                
                st.write(f"### 📈 Bullish Stocks (3-5% Up) in **{selected_list}**:")
                st.dataframe(df_up, use_container_width=True)

        # **Bearish Stocks**
        elif strategy == "📉 Bearish Stocks":
            df_down = clean_dataframe(stocks_down_3_to_5)
            if df_down.empty:
                st.warning(f"No bearish stocks in **{selected_list}** met the criteria.")
            else:
                search_down = st.text_input("🔍 Search Bearish Stock:").upper()
                if search_down:
                    df_down = df_down[df_down["Name"].str.contains(search_down, na=False, regex=False)]
                
                st.write(f"### 📉 Bearish Stocks (3-5% Down) in **{selected_list}**:")
                st.dataframe(df_down, use_container_width=True)
