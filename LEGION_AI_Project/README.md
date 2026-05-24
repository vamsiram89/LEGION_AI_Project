# LEGION AI – Life Emergency Guardian Agent

This repository contains a minimal yet functional implementation of **LEGION AI**, a privacy‑first agent designed to monitor early warning signals related to health, mental well‑being and financial stability.  The project is structured as a realistic MVP using a Python backend (FastAPI) and a simple Streamlit front‑end.  It is intended as a starting point for researchers and developers who want to explore the concepts outlined in the project plan described in the user document.

## Features (MVP)

* **User management:** basic registration and emergency contact management.
* **Data ingestion:** endpoints to submit wearable health metrics (heart rate, sleep hours), mood journal entries (free text) and spending logs (amount and category).
* **Risk scoring:** a lightweight risk engine calculates separate risk scores for health, mental stress and finances, then aggregates them into an overall score on a 0‑100 scale.  Scores fall into four bands: Safe (0–30), Watch (31–60), High Risk (61–80) and Emergency (81–100).
* **Anomaly detection:** a simple Isolation Forest model flags unusual spending behaviour; the Vader sentiment analyser estimates mood polarity from text; health risk is inferred using basic thresholds and time‑series anomalies.
* **Explanations:** an `explain_risk` function provides natural‑language rationale for the computed score, demonstrating how an LLM‑based agent could justify its recommendations.
* **Alerts:** when the overall score crosses the High Risk or Emergency thresholds the system sends a placeholder notification (replace with Twilio, email or WhatsApp integration).
* **Streamlit UI:** a minimal dashboard allows users to submit data and view their current risk status.

## Project structure

The project is divided into a backend and frontend:

```
LEGION_AI_Project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI entry point
│   │   ├── database.py        # SQLAlchemy models and DB session
│   │   ├── schemas.py         # Pydantic request/response models
│   │   ├── models.py          # SQLAlchemy ORM tables
│   │   ├── risk_engine.py     # Risk scoring logic
│   │   ├── ml_models.py       # Isolation Forest + sentiment analyser
│   │   ├── notifications.py   # Placeholder notification functions
│   │   └── utils.py           # Helper functions
│   ├── requirements.txt       # Backend dependencies
│   └── Dockerfile             # Containerise the backend
├── frontend/
│   ├── app.py                 # Streamlit UI
│   ├── requirements.txt       # Frontend dependencies
│   └── Dockerfile             # Containerise the frontend
└── README.md                  # This file
```

## Running locally

### Backend

1. Create a virtual environment and install dependencies:

```bash
cd LEGION_AI_Project/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

2. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  Interactive API docs can be accessed at `/docs`.

### Frontend

1. Install dependencies:

```bash
cd LEGION_AI_Project/frontend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

2. Launch the Streamlit app:

```bash
streamlit run app.py
```

The UI will open in your default web browser.  Configure the backend URL if running on a different host.

## Deployment

Dockerfiles are included for both the backend and frontend.  Build and run them using `docker compose` or deploy each container separately on your preferred cloud service (AWS EC2, ECS or Kubernetes).  For production you should replace the SQLite database with PostgreSQL or another RDBMS, configure environment variables (e.g., database URL, API keys), and secure the endpoints with proper authentication and HTTPS.

## Disclaimer

This project is for research and educational purposes only.  It is not a medical device and **must not** be used to diagnose disease or make clinical decisions.  All predictions are risk estimates based on limited data and should be reviewed by qualified professionals.  The system demonstrates a privacy‑first, consent‑driven approach consistent with data protection principles like HIPAA and India’s Digital Personal Data Protection Act 【951329831153024†L304-L339】.  It shows how AI can serve as a supportive tool rather than replacing human judgement 【44784662307980†L129-L135】.