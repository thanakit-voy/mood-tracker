import logging

from config import ACTIVITIES, GEMINI_API_KEY, MOODS

logger = logging.getLogger(__name__)

FALLBACK_QUOTES = {
    "happy": "You're shining bright today! Keep spreading that sunshine!",
    "sad": "It's okay to feel blue sometimes. Tomorrow can be a brand new day!",
    "excited": "Wow, your energy is amazing! Go chase those awesome dreams!",
    "calm": "You're doing great staying peaceful. Take a deep breath and smile!",
    "angry": "Big feelings are okay. Take a moment, then try something fun!",
    "tired": "Rest is super important. You deserve a cozy, happy break!",
}


def _build_prompt(mood: str, activity: str, message: str) -> str:
    mood_label = MOODS[mood]["label"]
    activity_label = ACTIVITIES[activity]["label"]
    return (
        f"You write short encouraging quotes for children (ages 6-12).\n"
        f"The child feels {mood_label} while {activity_label.lower()}.\n"
        f"They wrote: \"{message}\"\n\n"
        f"Write exactly ONE short encouraging quote (1-2 sentences, simple words).\n"
        f"Reference their mood, activity, and what they wrote.\n"
        f"Keep it positive, warm, and kid-friendly. No scary content.\n"
        f"Do NOT use markdown, quotation marks around the quote, or emojis.\n"
        f"Output only the quote text."
    )


def generate_quote(mood: str, activity: str, message: str) -> str:
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set, using fallback quote")
        return FALLBACK_QUOTES.get(mood, FALLBACK_QUOTES["happy"])

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = _build_prompt(mood, activity, message)

        for model in ("gemini-2.5-flash", "gemini-2.0-flash"):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                text = (response.text or "").strip()
                if text:
                    return text.strip('"\'')
            except Exception as e:
                logger.warning("Model %s failed: %s", model, e)
                continue

    except Exception as e:
        logger.error("Gemini API error: %s", e)

    return FALLBACK_QUOTES.get(mood, FALLBACK_QUOTES["happy"])
