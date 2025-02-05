# import openai
# import whisper
# import streamlit as st

# from src.utils.settings import OPENAI_API_KEY

# # Initialize Whisper model globally to avoid reloading it every time


# @st.cache_resource
# def load_whisper_model():
#     return whisper.load_model("base")  # Choose between "tiny", "base", "small", "medium", or "large"


# whisper_model = load_whisper_model()


# def transcribe_with_whisper(audio_path):
#     """
#     Transcribes audio using OpenAI's Whisper model.

#     Args:
#         audio_path (str): Path to the audio file to be transcribed.

#     Returns:
#         str: The transcribed text.
#     """
#     print("Transcribing audio with Whisper...", audio_path)
#     result = whisper_model.transcribe(audio_path)
#     return result["text"]


# client = openai.OpenAI(api_key=OPENAI_API_KEY)


# def transcribe_with_whisper_api(audio_path):
#     with open(audio_path, "rb") as audio_file:
#         response = client.audio.transcriptions.with_raw_response("whisper-1", audio_file, api_type="openai")
#     return response["text"]