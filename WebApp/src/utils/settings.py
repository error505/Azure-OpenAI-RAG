from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
AZURE_AI_SEARCH_API_KEY = os.getenv("AZURE_AI_SEARCH_API_KEY")
AZURE_AI_SEARCH_INDEX_NAME = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")

# Model configurations
AVAILABLE_MODELS = ["gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"]
API_OPTIONS = ["Azure OpenAI", "Native OpenAI"]
ALLOWED_FILE_TYPES = ["txt", "pdf", "docx", "md"]

# Default parameter values
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 256