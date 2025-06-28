import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROME_PATH = '/usr/bin/google-chrome'  # Linux Chrome path