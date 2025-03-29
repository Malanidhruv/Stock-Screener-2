import streamlit as st
import sqlite3
import datetime

# Connect to SQLite database (it will create one if it doesn't exist)
conn = sqlite3.connect("chat_messages.db")
c = conn.cursor()

# Create messages table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        message TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Display title
st.title("Group Chat - Stock Discussion")

# Initialize session state for user_id if it doesn't exist
if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{str(datetime.datetime.now().microsecond)}"

# Function to insert a message into the database
def add_message(user_id, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO messages (user_id, message, timestamp) VALUES (?, ?, ?)", (user_id, message, timestamp))
    conn.commit()

# Function to fetch all messages from the database
def get_messages():
    c.execute("SELECT user_id, message, timestamp FROM messages ORDER BY id ASC")
    return c.fetchall()

# User input for chat message
user_input = st.text_input("Enter your message:")

if user_input:
    add_message(st.session_state["user_id"], user_input)
    st.text_input("Enter your message:", value="", key="empty_input")  # Clear input box

# Display chat history
st.subheader("Chat History")
messages = get_messages()

for user, msg, timestamp in messages:
    st.write(f"[{timestamp}] **{user}**: {msg}")

# Close the connection when done
conn.close()
