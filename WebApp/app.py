import streamlit as st
from src.services.azure_ai_search import (
    create_index_if_not_exists,
    get_search_client,
)

from src.services.document_processor import process_file, create_documents
from src.utils.settings import (
    ALLOWED_FILE_TYPES
)
from src.ui.sidebar import render_sidebar
from src.ui.chat_interface import render_chat_interface

# Create index if not already created
create_index_if_not_exists()
search_client = get_search_client()
# Give title to the page
st.title("OpenAI ChatGPT with File Upload and Azure AI Search")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Render sidebar and get parameters
model_option, api_option, temperature, max_tokens = render_sidebar()

# File uploader functionality
uploaded_file = st.file_uploader("Upload a file", type=ALLOWED_FILE_TYPES)


if uploaded_file:
    # Process the file
    file_contents = process_file(uploaded_file)

    # Create documents for search indexing
    documents = create_documents(file_contents, uploaded_file)

    # Upload chunks to Azure AI Search
    search_client.upload_documents(documents=documents)

    st.sidebar.write("Uploaded chunks to Azure AI Search.")

# Update the interface with the previous messages
render_chat_interface(model_option, api_option, temperature, max_tokens)
