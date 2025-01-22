import streamlit as st
from src.services.auth import check_authentication
from src.services.azure_cosmos_db import get_chats  # Fetching conversations from CosmosDB
import uuid

from src.utils.settings import (
    AVAILABLE_MODELS,
    API_OPTIONS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS
)


def render_sidebar():
    # Render model selection and other parameters
    st.sidebar.title("ChatGPT Model Selection")
    model_option = st.sidebar.selectbox("Select Model", AVAILABLE_MODELS)
    
    api_option = st.sidebar.radio("Choose API", API_OPTIONS)
    
    st.sidebar.title("Model Parameters")
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=DEFAULT_TEMPERATURE,
        step=0.1
    )
    max_tokens = st.sidebar.slider(
        "Max Tokens",
        min_value=1,
        max_value=4096,
        value=DEFAULT_MAX_TOKENS
    )

    # Token usage and cost (initial values)
    st.sidebar.title("Token Usage and Cost")
    st.sidebar.write("Token usage and costs will be displayed here after querying.")

    # Ensure the user is authenticated before showing chats
    if not check_authentication():
        st.sidebar.write("Please log in to view your conversations.")
        return model_option, api_option, temperature, max_tokens, None
    
    user_id = st.session_state.get("user_id", None)
    if not user_id:
        st.sidebar.write("User ID not found. Please authenticate again.")
        return model_option, api_option, temperature, max_tokens, None

    # Display conversation list
    try:
        print("User ID:", user_id)
        conversations = get_chats(user_id)  # Pass user_id to get only their chats
        st.sidebar.write(f"Conversations found: {len(conversations)}")  # Log how many conversations are found

        # Extract conversation names (you can replace this with other identifiers if needed)
        conversation_names = [chat.get('name', f"Conversation {chat['id']}") for chat in conversations]  

        # Always create a new chat as the default selection
        conversation_names.insert(0, "Start a new conversation")

        selected_conversation_name = st.sidebar.selectbox("Select Conversation", conversation_names)

        # If "Start a new conversation" is selected, initialize a new chat
        if selected_conversation_name == "Start a new conversation":
            new_chat_id = str(uuid.uuid4())  # Generate new chat ID
            st.session_state["chat_id"] = new_chat_id
            st.session_state["current_chat"] = []  # Initialize an empty chat
            st.sidebar.write(f"Starting new conversation with ID: {new_chat_id}")
            selected_conversation = {"id": new_chat_id, "messages": []}  # Set default message as empty
        else:
            # Load the selected conversation
            selected_conversation = next(
                (chat for chat in conversations if chat.get('name', f"Conversation {chat['id']}") == selected_conversation_name),
                None  # Return None if not found
            )
            if selected_conversation is None:
                st.sidebar.write("Selected conversation could not be found.")
                selected_conversation = {"id": None, "messages": []}  # Set to empty if conversation is not found
            else:
                conversation_id = selected_conversation['id']
                st.session_state["chat_id"] = conversation_id  # Store the selected conversation ID
                st.sidebar.write(f"Currently viewing conversation: {selected_conversation_name} (ID: {conversation_id})")

    except Exception as e:
        st.sidebar.write(f"Error fetching conversations: {str(e)}")
        # Fallback: Start with a new conversation
        new_chat_id = str(uuid.uuid4())
        st.session_state["chat_id"] = new_chat_id
        st.session_state["current_chat"] = []  # Initialize an empty conversation
        selected_conversation = {"id": new_chat_id, "messages": []}  # Set default empty messages

    return model_option, api_option, temperature, max_tokens, selected_conversation
