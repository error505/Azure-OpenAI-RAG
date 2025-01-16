import streamlit as st
from src.services.azure_ai_search import (
    handle_upload_documents
)

from src.utils.settings import (
    ALLOWED_FILE_TYPES
)
from src.ui.sidebar import render_sidebar
from src.ui.chat_interface import render_chat_interface

# Give title to the page
st.title("OpenAI ChatGPT with File Upload and Azure AI Search")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Render sidebar and get parameters
model_option, api_option, temperature, max_tokens = render_sidebar()
# Update the interface with the previous messages
render_chat_interface(model_option, api_option, temperature, max_tokens)
# File uploader functionality
uploaded_file = st.file_uploader("Upload a file", type=ALLOWED_FILE_TYPES)
if uploaded_file:
    # Process the file
    handle_upload_documents(uploaded_file)

    st.sidebar.write("Uploaded chunks to Azure AI Search.")
