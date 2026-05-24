"""
SQLAlchemy ORM models for LEGION AI.

These models represent the core entities used by the system: users,
emergency contacts, health measurements, mood journals, spending logs,
risk scores and alerts.  Additional entities like permissions and audit
logs are included to support consent and traceability.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    emergency_contacts = relationship("EmergencyContact", back_populates="user")
    health_data = relationship("HealthData", back_populates="user")
    mood_logs = relationship("MoodLog", back_populates="user")
    spending_logs = relationship("SpendingLog", back_populates="user")
    risk_scores = relationship("RiskScore", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    consents = relationship("ConsentPermission", back_populates="user")
    actions = relationship("AgentAction", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    relation = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="emergency_contacts")


class HealthData(Base):
    __tablename__ = "health_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    heart_rate = Column(Float, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    steps = Column(Integer, nullable=True)
    bp_systolic = Column(Float, nullable=True)
    bp_diastolic = Column(Float, nullable=True)

    user = relationship("User", back_populates="health_data")


class MoodLog(Base):
    __tablename__ = "mood_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    text = Column(Text, nullable=False)
    sentiment_score = Column(Float, nullable=True)

    user = relationship("User", back_populates="mood_logs")


class SpendingLog(Base):
    __tablename__ = "spending_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    anomaly_score = Column(Float, nullable=True)

    user = relationship("User", back_populates="spending_logs")


class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    health_score = Column(Float)
    mood_score = Column(Float)
    finance_score = Column(Float)
    overall_score = Column(Float)
    level = Column(String)
    explanation = Column(Text)

    user = relationship("User", back_populates="risk_scores")


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(Text)
    level = Column(String)
    acknowledged = Column(Boolean, default=False)

    user = relationship("User", back_populates="alerts")


class ConsentPermission(Base):
    __tablename__ = "consent_permissions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission_type = Column(String)  # e.g., "share_with_family", "share_with_hospital"
    granted = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="consents")


class AgentAction(Base):
    __tablename__ = "agent_actions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    action_type = Column(String)  # e.g., "alert_sent", "recommendation_made"
    details = Column(Text)

    user = relationship("User", back_populates="actions")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event = Column(String)
    details = Column(Text)

    user = relationship("User", back_populates="audit_logs")