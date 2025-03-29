import streamlit as st

# Initialize session state variables if they don't already exist
if "session_id" not in st.session_state:
    st.session_state["session_id"] = "default_session"

if "user_id" not in st.session_state:
    st.session_state["user_id"] = f"User{st.session_state.session_id[:6]}"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("Anonymous Stock Discussion")

# User input for chat
user_input = st.text_input("Enter your message:")

if user_input:
    st.session_state["messages"].append(f"{st.session_state['user_id']}: {user_input}")
    st.text_input("Enter your message:", value="", key="empty_input")  # Clear input box

# Display chat history
st.subheader("Chat History")
for msg in st.session_state["messages"]:
    st.write(msg)
