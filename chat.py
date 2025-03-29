import streamlit as st
from datetime import datetime
import json
import os

# File path for chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Initialize session_id and user_id
if "session_id" not in st.session_state:
    st.session_state["session_id"] = os.urandom(16).hex()

if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{st.session_state.session_id[:6]}"

# Function to load chat history from the file
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save chat history to the file
def save_chat_history(messages):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(messages, file)

# Load chat history at the start
if "messages" not in st.session_state:
    st.session_state["messages"] = load_chat_history()

# Title and input section
st.title("Community Stock Discussion")

message = st.text_input("Enter your message", key="message_input")

if st.button("Send") and message:
    new_message = (st.session_state["user_id"], message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st.session_state["messages"].append(new_message)
    save_chat_history(st.session_state["messages"])
    st.experimental_rerun()

# Display all messages with timestamps
st.subheader("Chat Messages")
for user, msg, timestamp in st.session_state["messages"]:
    st.write(f"**{user}** [{timestamp}]: {msg}")
