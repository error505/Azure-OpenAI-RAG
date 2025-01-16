from openai import AzureOpenAI
from settings import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT


def create_azure_openai_client():
    """
    Create and return an AzureOpenAI client using managed identity.

    :return: An instance of AzureOpenAI client
    """
    try:
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version="2024-08-01-preview",
            api_key=AZURE_OPENAI_API_KEY,
        )
        return client
    except Exception as e:
        raise Exception(f"Error creating AzureOpenAI client: {e}")