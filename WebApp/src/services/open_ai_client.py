from openai import OpenAI
from src.services.settings import OPENAI_API_KEY


def create_chatgpt_openai_client():
    """
    Create and configure the OpenAI client for direct API use.

    :return: None (the `openai` library is globally configured)
    """
    try:
        # Create OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)
        client.embeddings.create(model="text-embedding-ada-002", input="test")
        print("OpenAI client created successfully.")
        return client
    except Exception as e:
        raise Exception(f"Error creating OpenAI client: {e}")