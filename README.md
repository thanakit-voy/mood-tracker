# Mood Tracker

A kid-friendly Flask app to track moods and activities, get encouraging AI-generated quotes from Google Gemini, and browse your quote history.

## Features

- Pick a mood and activity with big emoji buttons
- Write a short message about your day
- Get a personalized encouraging quote (powered by Gemini)
- Popup shows your special quote
- History saved to `data/history.json`
- App colors change based on your latest mood

## Setup

### 1. Create a virtual environment

```bash
cd mood-tracker
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API key

Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
cp .env.example .env
```

Edit `.env` and set your key:

```
GEMINI_API_KEY=your_actual_api_key_here
SECRET_KEY=any-random-string-for-flask
```

Without an API key, the app still works using built-in fallback quotes.

### 4. Run the app

```bash
flask --app app run --debug
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Project structure

```
mood-tracker/
├── app.py              # Flask routes
├── config.py           # Moods, activities, settings
├── services/
│   ├── gemini.py       # Quote generation
│   └── storage.py      # JSON history
├── data/history.json   # Saved entries (auto-created)
├── templates/          # HTML pages
└── static/             # CSS and JavaScript
```

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Home page |
| GET | `/history` | Quote history page |
| POST | `/api/generate` | Generate quote and save entry |
| GET | `/api/history` | JSON list of all entries |

### POST `/api/generate`

Request body:

```json
{
  "mood": "happy",
  "activity": "playing",
  "message": "I beat level 5!"
}
```

Response:

```json
{
  "id": "...",
  "created_at": "2026-05-29T12:00:00+00:00",
  "mood": "happy",
  "mood_emoji": "😊",
  "activity": "playing",
  "activity_emoji": "🎮",
  "message": "I beat level 5!",
  "quote": "You're a superstar gamer!"
}
```
