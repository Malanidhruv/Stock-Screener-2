import streamlit as st
from datetime import datetime
import os

# Initialize session_id if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state["session_id"] = os.urandom(16).hex()

if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{st.session_state.session_id[:6]}"
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Simple chat input and display area
st.title("Community Stock Discussion")
message = st.text_input("Enter your message", key="message_input")

if st.button("Send") and message:
    st.session_state["messages"].append((st.session_state["user_id"], message))
    st.experimental_rerun()

# Display messages
for user, msg in st.session_state["messages"]:
    st.write(f"{user}: {msg}")
