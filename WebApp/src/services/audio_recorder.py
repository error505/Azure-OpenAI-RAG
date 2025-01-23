import azure.cognitiveservices.speech as speechsdk
from src.utils.settings import AZURE_SPEECH_KEY, AZURE_SPEECH_ENDPOINT


def transcribe_with_azure(audio_stream):
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_ENDPOINT)
    audio_config = speechsdk.AudioConfig(filename=audio_stream)

    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation_details.reason}"




