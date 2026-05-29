import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
HISTORY_PATH = BASE_DIR / "data" / "history.json"
MAX_MESSAGE_LENGTH = 500

MOODS = {
    "happy": {"emoji": "😊", "label": "Happy"},
    "sad": {"emoji": "😢", "label": "Sad"},
    "excited": {"emoji": "🤩", "label": "Excited"},
    "calm": {"emoji": "😌", "label": "Calm"},
    "angry": {"emoji": "😤", "label": "Angry"},
    "tired": {"emoji": "😴", "label": "Tired"},
}

ACTIVITIES = {
    "playing": {"emoji": "🎮", "label": "Playing"},
    "reading": {"emoji": "📚", "label": "Reading"},
    "eating": {"emoji": "🍎", "label": "Eating"},
    "school": {"emoji": "🏫", "label": "School"},
    "sports": {"emoji": "⚽", "label": "Sports"},
    "sleeping": {"emoji": "😴", "label": "Sleeping"},
    "drawing": {"emoji": "🎨", "label": "Drawing"},
    "music": {"emoji": "🎵", "label": "Music"},
}
