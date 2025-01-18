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

        response, total_tokens, cost = get_chat_response(prompt, api_option, model_option, temperature, max_tokens)

        # Update the sidebar with token usage and cost information
        st.sidebar.write(f"Total Tokens Used: {total_tokens}")
        st.sidebar.write(f"Cost: ${cost:.4f}")  # Display cost with 4 decimal places
        add_message("assistant", response)

        with st.chat_message("assistant"):
            st.markdown(response)

