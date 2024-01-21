import os

import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set or is empty!")

openai.api_key = OPENAI_API_KEY

# for rapid and cheap development ise gpt-3.5-turbo
OPENAI_MODEL = "gpt-4-1106-preview"  # gpt-4-1106-preview
OPENAI_TEMPERATURE = 0

TO_MARKDOWN_API_KEY = os.getenv("TO_MARKDOWN_API_KEY")