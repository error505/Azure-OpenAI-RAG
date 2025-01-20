import uuid
import streamlit as st
from src.services.chat_service import get_chat_response
from src.utils.session_manager import add_message
from src.services.azure_cosmos_db import get_chats
from src.utils.session_manager import initialize_session_state


def render_chat_interface(model_option: str, api_option: str, temperature: float, max_tokens: int):
    # Ensure the session state is initialized
    initialize_session_state()

    # Fetch the current chat_id from session state (None means new conversation)
    conversation_id = st.session_state.get("chat_id", None)

    # If no conversation_id exists, start a new conversation
    if conversation_id is None:
        # Set a new conversation ID for this session
        st.session_state["chat_id"] = str(uuid.uuid4())  # New unique conversation ID
        messages = []  # Start with an empty conversation
    else:
        # Fetch the conversations from CosmosDB
        user_id = st.session_state.get("user_id", None)
        conversations = get_chats(user_id)

        # Select the conversation based on the ID
        selected_conversation = next((c for c in conversations if c["id"] == conversation_id), None)
        
        # If conversation exists, load the messages
        if selected_conversation:
            messages = selected_conversation["messages"]
        else:
            messages = []

    # Display existing messages in the chat
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new messages
    if prompt := st.chat_input("Enter your query"):
        # Add the new user message to the session state
        add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get chat response
        response, total_tokens, cost = get_chat_response(prompt, api_option, model_option, temperature, max_tokens)

        # Update the sidebar with token usage and cost information
        st.sidebar.write(f"Total Tokens Used: {total_tokens}")
        st.sidebar.write(f"Cost: ${cost:.4f}")

        # Add assistant's response to the conversation
        add_message("assistant", response)

        with st.chat_message("assistant"):
            st.markdown(response)
