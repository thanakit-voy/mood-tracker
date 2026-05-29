import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

import config
from services.gemini import generate_quote
from services.storage import append_entry, get_latest_mood, load_history

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def _validate_submission(data: dict):
    mood = data.get("mood", "").strip()
    activity = data.get("activity", "").strip()
    message = data.get("message", "").strip()

    if mood not in config.MOODS:
        return None, "Please pick a mood."
    if activity not in config.ACTIVITIES:
        return None, "Please pick an activity."
    if not message:
        return None, "Please write a message."
    if len(message) > config.MAX_MESSAGE_LENGTH:
        return None, f"Message is too long (max {config.MAX_MESSAGE_LENGTH} characters)."

    return mood, activity, message


@app.route("/")
def index():
    latest_mood = get_latest_mood() or "happy"
    return render_template(
        "index.html",
        moods=config.MOODS,
        activities=config.ACTIVITIES,
        latest_mood=latest_mood,
    )


@app.route("/history")
def history_page():
    entries = load_history()
    latest_mood = get_latest_mood() or "happy"
    return render_template(
        "history.html",
        entries=entries,
        latest_mood=latest_mood,
    )


@app.route("/api/history")
def api_history():
    return jsonify(load_history())


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}
    result = _validate_submission(data)

    if isinstance(result, tuple) and len(result) == 2:
        return jsonify({"error": result[1]}), 400

    mood, activity, message = result
    quote = generate_quote(mood, activity, message)

    entry = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mood": mood,
        "mood_emoji": config.MOODS[mood]["emoji"],
        "activity": activity,
        "activity_emoji": config.ACTIVITIES[activity]["emoji"],
        "message": message,
        "quote": quote,
    }
    append_entry(entry)

    return jsonify(entry)


if __name__ == "__main__":
    app.run(debug=True)
