import streamlit as st
import pandas as pd
from alice_client import initialize_alice
from stock_analysis import get_stocks_3_to_5_percent_up, get_stocks_3_to_5_percent_down
from stock_lists import STOCK_LISTS

# Set page configuration with legacy browser support
st.set_page_config(
    page_title="Stock Screener",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize AliceBlue API
try:
    alice = initialize_alice()
except Exception as e:
    st.error(f"⚠️ Failed to initialize AliceBlue API: {e}")
    alice = None

@st.cache_data(ttl=300)
def fetch_stocks(tokens):
    """Fetch stock data and handle errors gracefully."""
    try:
        if not alice:
            raise Exception("AliceBlue API is not initialized.")
        
        up_stocks = get_stocks_3_to_5_percent_up(alice, tokens)
        down_stocks = get_stocks_3_to_5_percent_down(alice, tokens)
        return up_stocks, down_stocks
    except Exception as e:
        st.error(f"⚠️ Error fetching stock data: {e}")
        return [], []

def clean_data(data):
    """Convert API response (list of dictionaries) to a structured DataFrame."""
    if not data or not isinstance(data, list):
        return pd.DataFrame(columns=["Name", "Token", "Close", "Change (%)"])
    
    try:
        df = pd.DataFrame(data)  # Directly convert list of dictionaries to DataFrame
        
        # Round Close Price to 2 decimal places
        df["Close"] = df["Close"].astype(float).round(2)

        # Format Change (%) with 2 decimal places and add percentage sign
        df["Change (%)"] = df["Change (%)"].astype(float).round(2)

        return df
    except Exception as e:
        st.error(f"⚠️ Error processing stock data: {e}")
        return pd.DataFrame(columns=["Name", "Token", "Close", "Change (%)"])


def safe_display(df, title):
    """Display stock data in a properly formatted Streamlit dataframe."""
    if df.empty:
        st.warning(f"No stocks found for {title}")
        return

    # Apply conditional formatting: Green for positive, Red for negative
    styled_df = df.style.applymap(
        lambda x: "color: green; font-weight: bold;" if x > 0 else "color: red; font-weight: bold;",
        subset=["Change (%)"]
    )

    # Display DataFrame with title
    st.markdown(f"## {title}")
    st.dataframe(styled_df, height=400, width=800)

# Streamlit App UI
st.title("📈 Stock Screener - Daily Movers")

# Selection Widgets
col1, col2 = st.columns(2)
with col1:
    selected_list = st.selectbox("📋 Select Stock List:", list(STOCK_LISTS.keys()))
with col2:
    strategy = st.selectbox("🎯 Select Strategy:", ["📈 Bullish Stocks", "📉 Bearish Stocks"])

if st.button("🚀 Start Screening", type="primary"):
    tokens = STOCK_LISTS.get(selected_list, [])
    
    if not tokens:
        st.warning(f"No stocks found for {selected_list}. Please check your stock list configuration.")
    else:
        stocks_up_3_to_5, stocks_down_3_to_5 = fetch_stocks(tokens)

        # Process and display data based on selected strategy
        if strategy == "📈 Bullish Stocks":
            st.write("🔍 Debug - Stocks Up (3-5%):", stocks_up_3_to_5)  # Only print when bullish is selected
            df = clean_data(stocks_up_3_to_5)
            if not df.empty:
                search = st.text_input("🔍 Search Bullish Stocks:").upper()
                if search:
                    df = df[df["Name"].str.contains(search, na=False, regex=False)]
                safe_display(df, f"📈 Bullish Stocks (3-5% Up) in {selected_list}")
            else:
                st.warning(f"No bullish stocks found in {selected_list}")

        elif strategy == "📉 Bearish Stocks":
            st.write("🔍 Debug - Stocks Down (3-5%):", stocks_down_3_to_5)  # Only print when bearish is selected
            df = clean_data(stocks_down_3_to_5)
            if not df.empty:
                search = st.text_input("🔍 Search Bearish Stocks:").upper()
                if search:
                    df = df[df["Name"].str.contains(search, na=False, regex=False)]
                safe_display(df, f"📉 Bearish Stocks (3-5% Down) in {selected_list}")
            else:
                st.warning(f"No bearish stocks found in {selected_list}")

# Mobile-friendly CSS
st.markdown("""
<style>
@media screen and (max-width: 600px) {
    .table-wrapper table {
        font-size: 14px;
    }
    .table-wrapper td, .table-wrapper th {
        padding: 6px !important;
    }
}
</style>
""", unsafe_allow_html=True)
