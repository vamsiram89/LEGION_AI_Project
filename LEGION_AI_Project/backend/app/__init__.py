"""
LEGION AI backend package.

This package contains the FastAPI application and supporting modules for
ingesting user data, computing risk scores, generating explanations and
sending notifications.  The implementation demonstrates a privacy‑conscious
approach using SQLAlchemy for persistence, Pydantic models for data
validation, and simple machine learning models for anomaly detection.
"""

from .main import app  # noqa: F401