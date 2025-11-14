# CustomerAI – FastAPI Edition

This project is a lightweight but realistic customer behaviour recommender
built with **FastAPI** and a simple web UI.

- Backend: FastAPI (no API keys required)
- Frontend: Vanilla HTML/CSS/JS
- Data: CSV file at `customerai/data/events.csv`

## Setup

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn customerai.api.main:app --reload
```

API will be available at:

- http://127.0.0.1:8000/api/health
- http://127.0.0.1:8000/api/recommend

Interactive docs:

- http://127.0.0.1:8000/docs

## Run the demo UI

1. Start the API as shown above.
2. Open `customerai/frontend/index.html` in your browser.
3. Enter a user ID from the CSV (e.g. 101, 103) and click **Get recommendations**.
