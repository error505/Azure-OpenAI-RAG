import io
import streamlit as st
from src.services.azure_ai_search import handle_upload_documents
from src.utils.settings import ALLOWED_FILE_TYPES
from src.ui.sidebar import render_sidebar
from src.ui.chat_interface import render_chat_interface
from src.services.auth import display_authenticated_content, check_authentication, handle_github_callback  # Import functions

# Check if the user is authenticated at the start
if not check_authentication():  # Use check_authentication() here to check if the user is authenticated
    handle_github_callback()  # Check if we need to process a GitHub callback
    display_authenticated_content()  # Show the authentication process
else:
    # If authenticated, show the landing page content
    st.title("OpenAI ChatGPT with File Upload and Azure AI Search")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Render sidebar and get parameters
    model_option, api_option, temperature, max_tokens, conversation_id = render_sidebar()

    # Handle file uploads
    uploaded_file = st.file_uploader("Upload a file", type=ALLOWED_FILE_TYPES)
    render_chat_interface(model_option, api_option, temperature, max_tokens)

    # File uploader functionality
    if uploaded_file:
        # Process the file
        type_of_file = uploaded_file.type
        print("Uploaded file type:", type_of_file)
        name = uploaded_file.name
        file_stream = io.BytesIO(uploaded_file.getvalue())
        handle_upload_documents(file_stream, type_of_file, name)
        st.sidebar.write("Uploaded chunks to Azure AI Search.")
