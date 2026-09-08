# Triage App

## Aim

This project is a learning exercise to build a patient triage application. Its long-term goal is to help direct patients toward appropriate services based on the severity of their reported observations and symptoms.

The current version is an early minimum viable product (MVP). It accepts a small set of vital observations and assigns a triage category and priority using simple rule-based thresholds.

Future ideas include connecting patients with relevant NHS services, such as virtual consultations, live waiting information, and appointment booking. These integrations are not currently implemented.

## Current MVP

The API currently:

- Accepts heart rate, temperature, respiratory rate, oxygen saturation, chest pain, and an optional patient ID.
- Assigns `RED`, `ORANGE`, `YELLOW`, or `GREEN` triage categories.
- Returns a priority and a short reason for the assessment.
- Protects the triage endpoint with an API key.
- Includes tests for the core triage rules and threshold boundaries.

## Important Disclaimer

This project is for my own learning and development only. It is not a medical device, clinical decision-support system, or substitute for professional medical advice. It must not be used by NHS departments, healthcare departments, clinicians, patients, or members of the public to make real clinical decisions.

The rules and thresholds are simplified examples and have not been clinically validated. Do not enter real patient information or sensitive personal data into this project.

## Project Structure

```text
triage-app/
├── app/
│   ├── main.py       # FastAPI application and endpoints
│   ├── models.py     # Request data models
│   └── triage.py     # Triage categories and assessment rules
├── tests/
│   └── test_triage.py # Tests for triage logic
└── requirements.txt
```

## Setup

Python 3.10 or newer is required.

From the `triage-app` directory, install the dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
```

## Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at <http://127.0.0.1:8000>. Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

The default development API key is `dev-demo-key`. The `/triage` endpoint requires it in an `X-API-Key` header. This default key is for local development only.

To use a different local key:

```bash
export TRIAGE_API_KEYS='your-local-key'
```

Do not commit real keys or `.env` files.

## Run Tests

```bash
pytest -v
```