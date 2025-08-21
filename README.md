# Kong Investment Quiz (Single‑Page App)

A minimal Streamlit single‑page application that collects a user's name and five multiple‑choice answers,
keeps question/answer data in a separate `questions.json`, and posts the selections to a Kong Gateway endpoint.

## Features

- Single page Streamlit UI themed with Kong colors and logo
- Name + 5 questions (one answer each)
- Question spec in JSON (`questions.json`) with short, professional labels and points
- POST to a configurable endpoint
- cURL preview and response viewer

## Local Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Configure Runtime

Override with `secrets.toml` file:

- `ENDPOINT_URL`
- `MESSAGES_TEMPLATE`
- `APIKEY`

## Deployment

Deployed to streamlit using Eugene's own github. Check with him for more details.

## Structure

```
.
├── .streamlit/
│   └── config.toml
├── assets/
│   └── kong-logo.png
├── app.py
├── questions.json
├── requirements.txt
├── Dockerfile
└── README.md
```
