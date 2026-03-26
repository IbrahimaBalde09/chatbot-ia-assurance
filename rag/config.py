from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
VECTORSTORE_DIR = BASE_DIR / "data" / "vectorstore"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4o-mini"

# Seuil simple pour décider si le contexte documentaire est suffisant
MIN_RELEVANCE_SCORE = 0.35