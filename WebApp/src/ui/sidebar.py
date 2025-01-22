import streamlit as st
import uuid
from src.services.auth import check_authentication
from src.services.azure_cosmos_db import get_chats

from src.utils.settings import (
    AVAILABLE_MODELS,
    API_OPTIONS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS
)

def render_sidebar():
    # Include Font Awesome styles
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
        """,
        unsafe_allow_html=True
    )

    # Sidebar Title
    st.sidebar.title("ChatGPT with File Upload")

    # Render sections with icons as markdown
    st.sidebar.markdown(
        """
        <div style="font-size: 18px; margin-bottom: 15px;">
            <i class="fas fa-cogs"></i> <b>Model Selection</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    model_option = st.sidebar.selectbox("Select Model", AVAILABLE_MODELS)
    api_option = st.sidebar.radio("Choose API", API_OPTIONS)

    st.sidebar.markdown(
        """
        <div style="font-size: 18px; margin-top: 25px; margin-bottom: 15px;">
            <i class="fas fa-thermometer-half"></i> <b>Model Parameters</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
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

    st.sidebar.markdown(
        """
        <div style="font-size: 18px; margin-top: 25px; margin-bottom: 15px;">
            <i class="fas fa-history"></i> <b>Chat History</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        conversations = get_chats(user_id)  # Pass user_id to get only their chats
        conversation_names = [chat.get('name', f"Conversation {chat['id']}") for chat in conversations]

        # Always create a new chat as the default selection
        conversation_names.insert(0, "Start a new conversation")

        selected_conversation_name = st.sidebar.selectbox("Select Conversation", conversation_names)

        # If "Start a new conversation" is selected, initialize a new chat
        if selected_conversation_name == "Start a new conversation":
            new_chat_id = str(uuid.uuid4())  # Generate new chat ID
            st.session_state["chat_id"] = new_chat_id
            st.session_state["current_chat"] = []  # Initialize an empty chat
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

    except Exception as e:
        st.sidebar.write(f"Error fetching conversations: {str(e)}")
        # Fallback: Start with a new conversation
        new_chat_id = str(uuid.uuid4())
        st.session_state["chat_id"] = new_chat_id
        st.session_state["current_chat"] = []  # Initialize an empty conversation
        selected_conversation = {"id": new_chat_id, "messages": []}  # Set default empty messages

    return model_option, api_option, temperature, max_tokens, selected_conversation
