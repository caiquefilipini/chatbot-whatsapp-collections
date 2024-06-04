import streamlit as st

# Persistent storage for conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Function to handle the chat process
def handle_chat():
    user_message = st.text_input("Please enter your message:", key="user_input")
    if user_message:
        # Simple constant response for demonstration
        bot_response = "Hello! I'm your friendly bot."
        st.session_state['history'].append({"user": user_message, "bot": bot_response})

        # Display bot response
        st.write(f"Bot: {bot_response}")

        # Rating input
        rating = st.slider("Please rate the response from 1 to 5:", 1, 5, key="rating")
        st.session_state['history'].append({"rating": rating})

# Display chat history
def display_history():
    for chat in st.session_state['history']:
        if 'user' in chat:
            st.text_area("User said:", value=chat['user'], height=50, disabled=True)
            st.text_area("Bot replied:", value=chat['bot'], height=50, disabled=True)
        if 'rating' in chat:
            st.write(f"Rating given: {chat['rating']}")

# Layout
st.title("Chatbot Interaction")
handle_chat()
display_history()
