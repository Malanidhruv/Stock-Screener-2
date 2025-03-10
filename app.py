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

st.set_page_config(page_title="Stock Screener", layout="wide")
st.title("📈 Stock Screener - Daily Movers")

# Centered Selection Widgets
selected_list = st.selectbox("📋 Select Stock List:", list(STOCK_LISTS.keys()))
strategy = st.selectbox("🎯 Select Strategy:", ["📈 Bullish Stocks", "📉 Bearish Stocks"])

if st.button("🚀 Start Screening"):
    tokens = STOCK_LISTS[selected_list]
    stocks_up_3_to_5, stocks_down_3_to_5 = fetch_stocks(tokens)

    def clean_dataframe(data):
        df = pd.DataFrame(data, columns=["Name", "Token", "Close", "Change (%)"])
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df["Change (%)"] = pd.to_numeric(df["Change (%)"], errors="coerce")
        df = df.fillna("").convert_dtypes()  # Convert to Arrow-friendly types
        return df

    if strategy == "📈 Bullish Stocks":
        if stocks_up_3_to_5:
            df_up = clean_dataframe(stocks_up_3_to_5)
            search_up = st.text_input("🔍 Search Stock:", "").upper()
            if search_up:
                df_up = df_up[df_up["Name"].str.contains(search_up, na=False)]

            st.write(f"### 📈 Bullish Stocks (3-5% Up) in **{selected_list}**:")

            # DEBUG: Print DataFrame to check if it's properly formatted
            st.write("🛠 Debugging: Raw DataFrame Output")
            st.write(df_up)  # 🔥 Debugging line

            # Alternative display methods for mobile compatibility
            st.table(df_up)  # ✅ Use static table for better support
            st.json(df_up.to_json(orient="records"))  # ✅ JSON Output

            # Main Display
            st.dataframe(df_up)  # 🚀 Main Display
        else:
            st.warning(f"No bullish stocks in **{selected_list}** met the criteria.")

    elif strategy == "📉 Bearish Stocks":
        if stocks_down_3_to_5:
            df_down = clean_dataframe(stocks_down_3_to_5)
            search_down = st.text_input("🔍 Search Stock:", "").upper()
            if search_down:
                df_down = df_down[df_down["Name"].str.contains(search_down, na=False)]

            st.write(f"### 📉 Bearish Stocks (3-5% Down) in **{selected_list}**:")

            # DEBUG: Print DataFrame to check if it's properly formatted
            st.write("🛠 Debugging: Raw DataFrame Output")
            st.write(df_down)  # 🔥 Debugging line

            # Alternative display methods for mobile compatibility
            st.table(df_down)  # ✅ Use static table for better support
            st.json(df_down.to_json(orient="records"))  # ✅ JSON Output

            # Main Display
            st.dataframe(df_down)  # 🚀 Main Display
        else:
            st.warning(f"No bearish stocks in **{selected_list}** met the criteria.")
