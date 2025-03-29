import streamlit as st
import requests
import json
import os

# Google Apps Script Web App URL (replace with your actual URL)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyjQqjHHBLLqQTfY9WpPCjDm7l_cg5qsYgyWxWXiQmpqbzSaiOqngEvmOAhzFJ8X26J/exec"

# Initialize session_id and user_id properly in session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = os.urandom(16).hex()

if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{st.session_state['session_id'][:6]}"

st.title("Community Stock Discussion")

# Input for message
message = st.text_input("Enter your message", key="message_input")

if st.button("Send") and message:
    # Send the message to Google Sheets through the web app
    response = requests.post(WEB_APP_URL, params={"action": "postMessage", "user": st.session_state["user_id"], "message": message})
    if response.status_code == 200:
        st.success("Message sent!")
    else:
        st.error("Failed to send the message. Try again.")

# Fetch and display chat messages
try:
    response = requests.get(WEB_APP_URL, params={"action": "getMessages"})
    if response.status_code == 200:
        messages = json.loads(response.text)  # Parse JSON response

        st.subheader("Chat Messages")
        for entry in messages:
            # Safeguard: Check the structure before unpacking
            if len(entry) == 3:
                timestamp, user, msg = entry
                st.write(f"**{user}**: {msg}")
            else:
                st.write(f"Invalid message format: {entry}")
    else:
        st.error("Failed to fetch messages.")
except Exception as e:
    st.error(f"An error occurred: {e}")
