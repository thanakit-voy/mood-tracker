import json
import os
import tempfile
from pathlib import Path

from config import HISTORY_PATH


def _ensure_data_dir() -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_history() -> list[dict]:
    _ensure_data_dir()
    if not HISTORY_PATH.exists():
        return []
    try:
        with open(HISTORY_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, OSError):
        return []


def append_entry(entry: dict) -> dict:
    history = load_history()
    history.insert(0, entry)
    _save_history(history)
    return entry


def _save_history(history: list[dict]) -> None:
    _ensure_data_dir()
    fd, tmp_path = tempfile.mkstemp(
        dir=HISTORY_PATH.parent, suffix=".tmp", text=True
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        Path(tmp_path).replace(HISTORY_PATH)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def get_latest_mood() -> str | None:
    history = load_history()
    if history:
        return history[0].get("mood")
    return None
