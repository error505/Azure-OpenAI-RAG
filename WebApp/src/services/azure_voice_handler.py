import azure.cognitiveservices.speech as speechsdk
from src.utils.settings import AZURE_SPEECH_KEY


def transcribe_with_azure(audio_path):
    """
    Transcribes audio using Azure Speech SDK.
    
    Args:
        audio_path (str): Path to the audio file to be transcribed.

    Returns:
        str: The transcribed text.
    """
    # Replace these with your Azure Speech resource credentials
    subscription_key = AZURE_SPEECH_KEY
    region = "germanywestcentral"

    # Configure the Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, speech_recognition_language="en-US", endpoint="https://germanywestcentral.api.cognitive.microsoft.com/")
    audio_config = speechsdk.AudioConfig(filename=audio_path)

    # Initialize the speech recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Perform the transcription
    result = speech_recognizer.recognize_once()

    # Check the result and return the text or handle errors
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        raise Exception("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Speech recognition canceled: {cancellation_details.reason}")
    else:
        raise Exception("Unknown error during transcription.")

