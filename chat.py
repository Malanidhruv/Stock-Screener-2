import streamlit as st
from datetime import datetime
import os

# File to store chat history (ensures messages persist)
CHAT_FILE = "chat_history.txt"

# Initialize session state for the user and messages
if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{os.urandom(4).hex()}"

if "messages" not in st.session_state:
    # Load messages from file or create empty list
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as file:
            st.session_state["messages"] = [line.strip().split("||") for line in file.readlines()]
    else:
        st.session_state["messages"] = []

# Save message to the chat history file
def save_message(user, msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(CHAT_FILE, "a") as file:
        file.write(f"{timestamp}||{user}||{msg}\n")

# Page layout
st.title("📈 Community Stock Discussion")
st.write("Join the discussion and share your stock trading thoughts!")

# Input area for sending messages
message = st.text_input("Type your message here...", key="message_input")

# Handle message sending
if st.button("Send") and message:
    user = st.session_state["user_id"]
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state["messages"].append((timestamp, user, message))
    save_message(user, message)
    st.experimental_rerun()  # Refresh the chat

# Display the chat messages
st.markdown("### 🗨️ Chat History")
if st.session_state["messages"]:
    for timestamp, user, msg in st.session_state["messages"]:
        st.write(f"**[{timestamp}] {user}:** {msg}")
else:
    st.write("No messages yet. Start the conversation!")

# Optional Clear Chat Button (Admin Only)
if st.button("Clear Chat (Admin)"):
    if os.path.exists(CHAT_FILE):
        os.remove(CHAT_FILE)
    st.session_state["messages"] = []
    st.experimental_rerun()
