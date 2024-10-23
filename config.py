import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_COLLECTION_NAME = "customer_support"
CHROMA_DB_DIR = "./chroma_db"  # Directory for Chroma's local database