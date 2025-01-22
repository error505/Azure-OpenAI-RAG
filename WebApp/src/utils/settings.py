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
AZURE_COSMOS_DB_CONNECTION_STRING = os.getenv("COSMOS_DB_CONNECTION_STRING")
AZURE_COSMOS_DB_DATABASE_NAME = os.getenv("DATABASE_NAME")
AZURE_COSMOS_DB_CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# Model configurations
AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-4o-mini", "o1-preview", "o1-mini"]
API_OPTIONS = ["Azure OpenAI", "Native OpenAI"]
ALLOWED_FILE_TYPES = ["txt", "pdf", "docx", "md", "html", "csv", "json", "jpg", "jpeg", "png"] 

# Default parameter values
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 256

# Auth
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")  # Replace with your GitHub OAuth client ID
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")  # Replace with your GitHub OAuth client secret
GITHUB_AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
