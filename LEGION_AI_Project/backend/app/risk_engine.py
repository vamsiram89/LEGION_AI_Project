"""
Risk scoring logic for LEGION AI.

This module provides functions to compute risk scores in the range 0–100 for
health, mood and financial domains based on simple heuristics and ML models.
The aggregate risk score is a weighted average of individual scores.  A
categorical level (Safe, Watch, High Risk, Emergency) is derived from the
overall score.  An explanation function generates a human‑readable rationale
for the computed scores.
"""

from typing import Optional, List, Dict
import numpy as np
from .ml_models import SpendingAnomalyModel, sentiment_score


def compute_health_score(heart_rate: Optional[float], sleep_hours: Optional[float], steps: Optional[int], bp_systolic: Optional[float], bp_diastolic: Optional[float]) -> float:
    """
    Compute a simple health risk score.

    The logic penalises very high or low heart rates, insufficient sleep, low
    activity and abnormal blood pressure.  Scores range from 0 (low risk) to 100
    (high risk).  Missing values reduce confidence but do not automatically
    imply risk.
    """
    score = 0.0
    weight_sum = 0.0

    # Heart rate (resting). Normal resting HR for adults is 60–100 bpm.
    if heart_rate is not None:
        weight_sum += 1
        if heart_rate < 50 or heart_rate > 100:
            score += 80  # high risk
        elif heart_rate < 60 or heart_rate > 90:
            score += 40  # moderate
        else:
            score += 10  # low risk

    # Sleep hours: optimal 7–9 hours
    if sleep_hours is not None:
        weight_sum += 1
        if sleep_hours < 4 or sleep_hours > 10:
            score += 80
        elif sleep_hours < 6 or sleep_hours > 9:
            score += 40
        else:
            score += 10

    # Steps/activity: below 3000 steps may indicate sedentary lifestyle
    if steps is not None:
        weight_sum += 1
        if steps < 2000:
            score += 70
        elif steps < 5000:
            score += 40
        else:
            score += 10

    # Blood pressure (systolic and diastolic)
    if bp_systolic is not None and bp_diastolic is not None:
        weight_sum += 1
        if bp_systolic > 180 or bp_diastolic > 120 or bp_systolic < 90 or bp_diastolic < 60:
            score += 80
        elif bp_systolic > 140 or bp_diastolic > 90:
            score += 50
        else:
            score += 10

    # Average the score across available signals
    if weight_sum == 0:
        return 0.0
    return float(score / weight_sum)


def compute_mood_score(sentiment: float) -> float:
    """
    Convert sentiment polarity (-1 to 1) into a risk score 0–100.  Negative
    sentiment increases risk; positive sentiment lowers risk.
    """
    # Map sentiment: -1 -> 100, 0 -> 50, 1 -> 0
    score = (1 - sentiment) * 50
    return float(max(0.0, min(100.0, score)))


def compute_finance_score(anomaly: float) -> float:
    """
    Convert an anomaly score in [0, 1] into a 0–100 risk score.  We map 0.6
    threshold to 60 (high) and 1 to 100 (emergency).  Low anomalies produce
    scores near 10.
    """
    if anomaly < 0.2:
        return 10.0 * anomaly  # near zero risk
    elif anomaly < 0.6:
        return 40.0 + (anomaly - 0.2) * 50  # 40–60
    else:
        return 60.0 + (anomaly - 0.6) * 100  # 60–100


def aggregate_scores(health: float, mood: float, finance: float) -> float:
    """
    Combine individual risk scores into an overall score using weights.  Health is
    weighted at 0.4, mood at 0.3 and finance at 0.3.
    """
    return float(0.4 * health + 0.3 * mood + 0.3 * finance)


def determine_level(score: float) -> str:
    """Return a risk level category based on the overall score."""
    if score <= 30:
        return "Safe"
    elif score <= 60:
        return "Watch"
    elif score <= 80:
        return "High Risk"
    else:
        return "Emergency"


def explain_risk(scores: Dict[str, float]) -> str:
    """
    Generate a simple explanation for the risk scores.  This function
    demonstrates how an LLM-based agent might justify its recommendations.
    """
    parts = []
    health = scores.get("health")
    mood = scores.get("mood")
    finance = scores.get("finance")

    # Interpret health score
    if health is not None:
        if health > 70:
            parts.append("Health readings suggest significant abnormalities (e.g., high/low heart rate, poor sleep or blood pressure). Consider consulting a doctor.")
        elif health > 40:
            parts.append("Some health metrics deviate from normal ranges. Try to improve sleep and monitor vital signs.")
        else:
            parts.append("Health metrics appear within normal ranges.")

    # Interpret mood score
    if mood is not None:
        if mood > 70:
            parts.append("Mood logs exhibit strong negative sentiment, which may indicate stress or depressive thoughts.")
        elif mood > 40:
            parts.append("Mood sentiment is somewhat negative. Engage in relaxation or talk to someone you trust.")
        else:
            parts.append("Mood appears generally positive or neutral.")

    # Interpret finance score
    if finance is not None:
        if finance > 70:
            parts.append("Spending behaviour is highly anomalous. Review recent transactions for fraud or overspending.")
        elif finance > 40:
            parts.append("Some unusual spending patterns detected. Keep an eye on your expenses.")
        else:
            parts.append("No financial anomalies detected.")

    return " ".join(parts)