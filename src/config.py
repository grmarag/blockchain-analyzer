import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()
logger.info("Environment variables loaded from the .env file.")

class Config:
    # OpenAI API key is loaded from the .env file
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        logger.error("OPENAI_API_KEY is not set in the .env file.")
        raise ValueError("Please set your OPENAI_API_KEY in the .env file.")
    else:
        logger.info("OPENAI_API_KEY successfully loaded.")