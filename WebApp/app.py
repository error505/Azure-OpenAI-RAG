import io
import os
import streamlit as st
# from audio_recorder_streamlit import audio_recorder
from src.services.azure_ai_search import handle_upload_documents
from src.ui.sidebar import render_sidebar
from src.ui.chat_interface import render_chat_interface
from src.services.auth import (
    display_authenticated_content,
    check_authentication,
    handle_github_callback,
)
# from src.services.whisper_handler import transcribe_with_whisper_api

# from src.services.azure_voice_handler import transcribe_with_azure


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check if the user is authenticated at the start
if not check_authentication():
    handle_github_callback()  # Check if we need to process a GitHub callback
    display_authenticated_content()  # Show the authentication process
else:
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Render sidebar and get parameters
    model_option, api_option, temperature, max_tokens, conversation_id = (
        render_sidebar()
    )

    # Handle file uploads
    uploaded_file = st.file_uploader(
        "Upload a file", type=["txt", "pdf", "wav", "mp3", "mp4"]
    )
    render_chat_interface(model_option, api_option, temperature, max_tokens)

    # File uploader functionality
    if uploaded_file:
        # Process the file
        type_of_file = uploaded_file.type
        name = uploaded_file.name
        file_stream = io.BytesIO(uploaded_file.getvalue())
        handle_upload_documents(file_stream, type_of_file, name)
        st.sidebar.write("Uploaded chunks to Azure AI Search.")

    # # Audio Recording Section
    # st.header("Record and Process Audio")
    # audio_data = audio_recorder(pause_threshold=0.5)

    # if audio_data:
    #     # Save the audio file to an absolute path
    #     audio_file_path = os.path.join(BASE_DIR, "temp_audio.wav")
    #     with open(audio_file_path, "wb") as f:
    #         f.write(audio_data)

    #     try:
    #         # Trascribe the recorded audio using Azure
    #         # transcribed_text = transcribe_with_azure(audio_stream)

    #         # Transcribe the recorded audio using Whisper
    #         transcribed_text = transcribe_with_whisper_api(audio_file_path)

    #         st.write("Transcribed Text from Audio:")
    #         st.text(transcribed_text)

    #         # Save the transcription in session state
    #         st.session_state["messages"] = [transcribed_text]
    #     except Exception as e:
    #         st.error(f"Error during transcription: {e}")
    #         st.stop()
