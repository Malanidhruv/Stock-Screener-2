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
alice = initialize_alice()

# Add polyfill warning
st.markdown("""
<script>
if (!Array.prototype.at) {
    alert('For best experience, use latest Chrome/Firefox. Some features may be limited.');
}
</script>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def fetch_stocks(tokens):
    try:
        return get_stocks_3_to_5_percent_up(alice, tokens), get_stocks_3_to_5_percent_down(alice, tokens)
    except Exception as e:
        st.error(f"⚠️ Error fetching stock data: {e}")
        return [], []

def safe_display(df, title):
    """Browser-safe table display with fallback"""
    if df.empty:
        return
    
    # Convert to HTML with basic styling
    html = f"""
    <div class="table-wrapper">
        <h3>{title}</h3>
        <table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
            <thead>
                <tr style="background: #f0f2f6;">{''.join(f'<th style="padding: 8px; border: 1px solid #ddd;">{col}</th>' for col in df.columns)}</tr>
            </thead>
            <tbody>
                {"".join(
                    f'<tr>{"".join(f"<td style=\"padding: 8px; border: 1px solid #ddd;\">{value}</td>" for value in row)}</tr>'
                    for row in df.values
                )}
            </tbody>
        </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

st.title("📈 Stock Screener - Daily Movers")

# Selection Widgets
col1, col2 = st.columns(2)
with col1:
    selected_list = st.selectbox("📋 Select Stock List:", list(STOCK_LISTS.keys()))
with col2:
    strategy = st.selectbox("🎯 Select Strategy:", ["📈 Bullish Stocks", "📉 Bearish Stocks"])

if st.button("🚀 Start Screening", type="primary"):
    tokens = STOCK_LISTS[selected_list]
    stocks_up_3_to_5, stocks_down_3_to_5 = fetch_stocks(tokens)

    def clean_data(data):
        return pd.DataFrame(
            [(item[0], str(item[1]), f"{item[2]:.2f}", f"{item[3]:.2f}%") 
             for item in data],
            columns=["Name", "Token", "Close", "Change (%)"]
        )

    if strategy == "📈 Bullish Stocks":
        df = clean_data(stocks_up_3_to_5)
        if not df.empty:
            search = st.text_input("🔍 Search Bullish Stocks:").upper()
            if search:
                df = df[df["Name"].str.contains(search, na=False, regex=False)]
            safe_display(df, f"📈 Bullish Stocks (3-5% Up) in {selected_list}")
        else:
            st.warning(f"No bullish stocks found in {selected_list}")

    elif strategy == "📉 Bearish Stocks":
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
