import streamlit as st
from datetime import datetime, timedelta

st.title("Anonymous Stock Discussion")

# Generate a random anonymous user ID if not already assigned
if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{st.session_state.session_id[:6]}"

# Temporary storage for chat messages (will reset on app restart)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat Input Section
with st.form("chat_form", clear_on_submit=True):
    message = st.text_input("Send a message anonymously")
    submit_button = st.form_submit_button("Send")

# Add the message if user submits
if submit_button and message:
    st.session_state["messages"].append({
        "user": st.session_state["user_id"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message
    })

# Display chat messages
st.write("### Chat Messages")
for msg in st.session_state["messages"]:
    st.markdown(f"**{msg['user']}** ({msg['timestamp']}): {msg['message']}")

# Auto-clear chat messages every 24 hours (based on timestamp)
if "last_clear" not in st.session_state:
    st.session_state["last_clear"] = datetime.now()

if datetime.now() > st.session_state["last_clear"] + timedelta(days=1):
    st.session_state["messages"] = []
    st.session_state["last_clear"] = datetime.now()
