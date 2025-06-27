import os
from dotenv import load_dotenv
load_dotenv()

DOCS_DIR = os.getenv("DOCS_DIR", "./docs")

HTTP_PORT = os.getenv("HTTP_PORT", 7654)

CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")