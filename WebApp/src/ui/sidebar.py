import streamlit as st
from src.services.settings import (
    AVAILABLE_MODELS,
    API_OPTIONS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS
)


def render_sidebar():
    # st.sidebar.title("OpenAI ChatGPT with File Upload and Azure AI Search")
    # logo_url = "https://animatesvg.error505.com/logo.png"
    # st.sidebar.image(logo_url, width=75)
    st.sidebar.title("ChatGPT Model Selection")
    model_option = st.sidebar.selectbox("Select Model", AVAILABLE_MODELS)
    
    api_option = st.sidebar.radio("Choose API", API_OPTIONS)
    
    st.sidebar.title("Model Parameters")
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=DEFAULT_TEMPERATURE,
        step=0.1
    )
    max_tokens = st.sidebar.slider(
        "Max Tokens",
        min_value=1,
        max_value=4096,
        value=DEFAULT_MAX_TOKENS
    )
    
    return model_option, api_option, temperature, max_tokens
