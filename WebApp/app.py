import io
import streamlit as st
from src.services.azure_ai_search import handle_upload_documents
from src.utils.settings import ALLOWED_FILE_TYPES
from src.ui.sidebar import render_sidebar
from src.ui.chat_interface import render_chat_interface
from src.services.auth import display_authenticated_content, check_authentication, handle_github_callback 
from src.services.audio_recorder import transcribe_with_azure
from audio_recorder_streamlit import audio_recorder


# Check if the user is authenticated at the start
if not check_authentication():  # Use check_authentication() here to check if the user is authenticated
    handle_github_callback()  # Check if we need to process a GitHub callback
    display_authenticated_content()  # Show the authentication process
else:
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

    # Audio Recording Section
    st.header("Record and Process Audio")
    audio_data = audio_recorder(pause_threshold=0.5)

if audio_data:
    st.audio(audio_data, format="audio/wav")
    audio_stream = "temp_audio.wav"

    with open(audio_stream, "wb") as f:
        f.write(audio_data)

    try:
        transcribed_text = transcribe_with_azure(audio_stream)
        st.write("Transcribed Text from Audio:")
        st.text(transcribed_text)

        st.session_state["messages"] = [transcribed_text]
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        st.write("Please try again.")
        st.stop()
