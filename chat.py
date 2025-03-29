import streamlit as st
import requests
import json

# Web app URL from Google Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyjQqjHHBLLqQTfY9WpPCjDm7l_cg5qsYgyWxWXiQmpqbzSaiOqngEvmOAhzFJ8X26J/exec"

# Initialize user ID in session state
if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{st.session_state.session_id[:6]}"

st.title("Community Stock Discussion")
message = st.text_input("Enter your message", key="message_input")

if st.button("Send") and message:
    # POST request to Google Apps Script (send message)
    response = requests.post(WEB_APP_URL, params={"action": "postMessage", "user": st.session_state["user_id"], "message": message})
    if response.status_code == 200:
        st.success("Message sent!")
    else:
        st.error("Failed to send message. Try again.")

# Fetch and display chat messages
try:
    response = requests.get(WEB_APP_URL, params={"action": "getMessages"})
    messages = json.loads(response.text)
    for timestamp, user, msg in messages:
        st.write(f"**{user}**: {msg}")
except Exception as e:
    st.error(f"Failed to fetch messages: {e}")
