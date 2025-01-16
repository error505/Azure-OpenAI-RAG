import streamlit as st
from src.services.chat_service import get_chat_response
from src.utils.session_manager import get_messages, add_message


def render_chat_interface(model_option: str, api_option: str, temperature: float, max_tokens: int):
    # Display existing messages
    for message in get_messages():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new messages
    if prompt := st.chat_input("Enter your query"):
        add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display assistant response
        assistant_reply = get_chat_response(
            prompt, api_option, model_option, temperature, max_tokens
        )
        add_message("assistant", assistant_reply)
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
