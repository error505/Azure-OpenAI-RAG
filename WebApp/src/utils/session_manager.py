import streamlit as st
from typing import List, Dict


def get_session_state() -> st.session_state:
    """Get the current session state."""
    return st.session_state


def initialize_session_state() -> None:
    """Initialize session state variables if they don't exist."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []


def get_messages() -> List[Dict[str, str]]:
    """Get all messages from the session state."""
    initialize_session_state()
    return st.session_state.messages


def add_message(role: str, content: str) -> None:
    """Add a new message to the session state."""
    initialize_session_state()
    st.session_state.messages.append({"role": role, "content": content})
    st.session_state.conversation_history.append({"role": role, "content": content})


def clear_conversation() -> None:
    """Clear the conversation history."""
    initialize_session_state()
    st.session_state.messages = []
    st.session_state.conversation_history = []


def get_conversation_context(max_length: int = 5) -> List[Dict[str, str]]:
    """Get recent conversation context."""
    initialize_session_state()
    return st.session_state.conversation_history[-max_length:]
