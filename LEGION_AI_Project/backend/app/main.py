"""
FastAPI application for the LEGION AI MVP.

This API exposes endpoints for user registration, data submission and risk
assessment.  It uses SQLAlchemy for persistence and simple ML models for
anomaly detection and sentiment analysis.  Risk scores are computed on
demand and stored in the database for historical review.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os

from . import models, schemas
from .database import Base, engine, get_db
from .risk_engine import compute_health_score, compute_mood_score, compute_finance_score, aggregate_scores, determine_level, explain_risk
from .ml_models import SpendingAnomalyModel, sentiment_score
from .utils import get_recent_health_data, get_recent_mood_logs, get_recent_spending
from .notifications import send_alert


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="LEGION AI Backend", version="0.1")


@app.post("/users", response_model=schemas.User, summary="Register a new user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User(name=user.name, email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/users/{user_id}/contacts", response_model=schemas.EmergencyContact, summary="Add an emergency contact")
def add_contact(user_id: int, contact: schemas.EmergencyContactCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_contact = models.EmergencyContact(user_id=user_id, name=contact.name, relation=contact.relation, phone=contact.phone, email=contact.email)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@app.post("/users/{user_id}/health", response_model=schemas.HealthData, summary="Submit health data")
def submit_health(user_id: int, data: schemas.HealthDataCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_data = models.HealthData(user_id=user_id, heart_rate=data.heart_rate, sleep_hours=data.sleep_hours, steps=data.steps, bp_systolic=data.bp_systolic, bp_diastolic=data.bp_diastolic)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


@app.post("/users/{user_id}/mood", response_model=schemas.MoodLog, summary="Submit a mood journal entry")
def submit_mood(user_id: int, log: schemas.MoodLogCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Compute sentiment
    sentiment = sentiment_score(log.text)
    db_log = models.MoodLog(user_id=user_id, text=log.text, sentiment_score=sentiment)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@app.post("/users/{user_id}/spending", response_model=schemas.SpendingLog, summary="Submit a spending record")
def submit_spending(user_id: int, log: schemas.SpendingLogCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Fit anomaly model on existing spending amounts
    past = [s.amount for s in db.query(models.SpendingLog).filter(models.SpendingLog.user_id == user_id).all()]
    model = SpendingAnomalyModel()
    model.fit(past)
    anomaly = model.score(log.amount)
    db_log = models.SpendingLog(user_id=user_id, amount=log.amount, category=log.category, anomaly_score=anomaly)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@app.get("/users/{user_id}/risk", response_model=schemas.RiskScore, summary="Calculate current risk score")
def calculate_risk(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Use the latest health data
    health_data = db.query(models.HealthData).filter(models.HealthData.user_id == user_id).order_by(models.HealthData.timestamp.desc()).first()
    if health_data:
        health_score = compute_health_score(health_data.heart_rate, health_data.sleep_hours, health_data.steps, health_data.bp_systolic, health_data.bp_diastolic)
    else:
        health_score = 0.0

    # Use average sentiment over last few mood logs
    mood_logs = db.query(models.MoodLog).filter(models.MoodLog.user_id == user_id).order_by(models.MoodLog.timestamp.desc()).limit(5).all()
    if mood_logs:
        avg_sentiment = sum(m.sentiment_score or 0.0 for m in mood_logs) / len(mood_logs)
        mood_score = compute_mood_score(avg_sentiment)
    else:
        mood_score = 0.0

    # Use the last spending anomaly score
    spending_log = db.query(models.SpendingLog).filter(models.SpendingLog.user_id == user_id).order_by(models.SpendingLog.timestamp.desc()).first()
    if spending_log:
        finance_score = compute_finance_score(spending_log.anomaly_score or 0.0)
    else:
        finance_score = 0.0

    overall = aggregate_scores(health_score, mood_score, finance_score)
    level = determine_level(overall)
    explanation = explain_risk({"health": health_score, "mood": mood_score, "finance": finance_score})

    # Persist the risk score
    risk = models.RiskScore(user_id=user_id, health_score=health_score, mood_score=mood_score, finance_score=finance_score, overall_score=overall, level=level, explanation=explanation)
    db.add(risk)
    db.commit()
    db.refresh(risk)

    # If risk high send alert
    if level in ("High Risk", "Emergency"):
        # Fetch contacts
        contacts = db.query(models.EmergencyContact).filter(models.EmergencyContact.user_id == user_id).all()
        message = f"LEGION AI detected a {level} situation for {user.name}: {explanation}. Risk score: {overall:.1f}."
        for c in contacts:
            send_alert({"name": c.name, "phone": c.phone, "email": c.email}, message)
        alert = models.Alert(user_id=user_id, message=message, level=level)
        db.add(alert)
        db.commit()

    return risk


@app.get("/users/{user_id}/history", response_model=List[schemas.RiskScore], summary="Retrieve risk history")
def get_risk_history(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    history = db.query(models.RiskScore).filter(models.RiskScore.user_id == user_id).order_by(models.RiskScore.timestamp.desc()).all()
    return history