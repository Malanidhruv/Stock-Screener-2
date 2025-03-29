import streamlit as st
from datetime import datetime
import os

# Persistent chat history (if you want to store chats permanently)
CHAT_FILE = "chat_history.txt"

# Initialize session states: User ID, session, and messages
if "session_id" not in st.session_state:
    st.session_state["session_id"] = os.urandom(16).hex()

if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{st.session_state.session_id[:6]}"

if "messages" not in st.session_state:
    # Load previous messages from file or create an empty list
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            st.session_state["messages"] = [line.strip().split("||") for line in f.readlines()]
    else:
        st.session_state["messages"] = []

# Function to save chat to a file for persistence
def save_chat(user, msg):
    with open(CHAT_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp}||{user}||{msg}\n")

# Page title and chat layout
st.title("📈 Community Stock Discussion Group Chat")

# Message input and send button
message = st.text_input("Enter your message", key="message_input")

if st.button("Send", key="send_button") and message:
    user = st.session_state["user_id"]
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Append message with timestamp to session state and file
    st.session_state["messages"].append((timestamp, user, message))
    save_chat(user, message)
    
    # Reset text input after sending the message
    st.experimental_rerun()

# Display chat history (newest messages at the bottom)
st.markdown("### 🗨️ Chat History")
if st.session_state["messages"]:
    chat_container = st.container()
    for timestamp, user, msg in st.session_state["messages"]:
        chat_container.write(f"**[{timestamp}] {user}:** {msg}")
else:
    st.write("No messages yet. Start the conversation!")

# Allow clearing chat (admin functionality)
if st.button("Clear Chat (Admin Only)"):
    if os.path.exists(CHAT_FILE):
        os.remove(CHAT_FILE)
    st.session_state["messages"] = []
    st.experimental_rerun()

# Optional styling to make it more appealing
st.markdown(
    """
    <style>
    div.stTextInput > div:first-child { border-radius: 12px; padding: 8px; }
    div[data-testid="stText"] { font-size: 1.1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
