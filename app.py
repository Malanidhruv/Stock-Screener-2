import streamlit as st
import pandas as pd
from alice_client import initialize_alice
from stock_analysis import get_stocks_3_to_5_percent_up, get_stocks_3_to_5_percent_down
from stock_lists import STOCK_LISTS

# Initialize AliceBlue API
alice = initialize_alice()

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_stocks(tokens):
    return get_stocks_3_to_5_percent_up(alice, tokens), get_stocks_3_to_5_percent_down(alice, tokens)

# Streamlit Setup
st.set_page_config(page_title="Stock Screener", layout="wide")
st.title("📈 Stock Screener - Daily Movers")

# Centering the selection widgets
col1, col2 = st.columns([1, 1])  # Two equal columns

with col1:
    selected_list = st.selectbox("📋 Select Stock List:", list(STOCK_LISTS.keys()))

with col2:
    strategy = st.selectbox("🎯 Select Strategy:", ["📈 Bullish Stocks", "📉 Bearish Stocks"])

# Centering the button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
start_button = st.button("🚀 Start Screening")
st.markdown("</div>", unsafe_allow_html=True)

# Fetch Data on Button Click
if start_button:
    tokens = STOCK_LISTS[selected_list]
    stocks_up_3_to_5, stocks_down_3_to_5 = fetch_stocks(tokens)  # Cached API call

    if strategy == "📈 Bullish Stocks":
        if stocks_up_3_to_5:
            df_up = pd.DataFrame(stocks_up_3_to_5, columns=["Name", "Token", "Close", "Change (%)"])
            search_up = st.text_input("🔍 Search Stock:", "").upper()
            if search_up:
                df_up = df_up[df_up["Name"].str.contains(search_up, na=False)]
            st.write(f"### 📈 Bullish Stocks (3-5% Up) in **{selected_list}**:")
            st.dataframe(df_up.style.format({"Close": "{:.2f}", "Change (%)": "{:.2f}"}))
        else:
            st.warning(f"No bullish stocks in **{selected_list}** met the criteria.")

    elif strategy == "📉 Bearish Stocks":
        if stocks_down_3_to_5:
            df_down = pd.DataFrame(stocks_down_3_to_5, columns=["Name", "Token", "Close", "Change (%)"])
            search_down = st.text_input("🔍 Search Stock:", "").upper()
            if search_down:
                df_down = df_down[df_down["Name"].str.contains(search_down, na=False)]
            st.write(f"### 📉 Bearish Stocks (3-5% Down) in **{selected_list}**:")
            st.dataframe(df_down.style.format({"Close": "{:.2f}", "Change (%)": "{:.2f}"}))
        else:
            st.warning(f"No bearish stocks in **{selected_list}** met the criteria.")
