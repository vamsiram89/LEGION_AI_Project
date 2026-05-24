"""
Pydantic models for request and response bodies used by the API.

Separate schemas are defined for creation/update operations (input models) and
responses (output models).  Default values and validators ensure that basic
validation happens before data reaches the business logic layer.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


# ---------- User and Contacts ----------

class EmergencyContactBase(BaseModel):
    name: str
    relation: Optional[str] = None
    phone: str
    email: Optional[EmailStr] = None


class EmergencyContactCreate(EmergencyContactBase):
    pass


class EmergencyContact(EmergencyContactBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    emergency_contacts: List[EmergencyContact] = []

    class Config:
        orm_mode = True


# ---------- Health Data ----------

class HealthDataBase(BaseModel):
    heart_rate: Optional[float] = None
    sleep_hours: Optional[float] = None
    steps: Optional[int] = None
    bp_systolic: Optional[float] = None
    bp_diastolic: Optional[float] = None


class HealthDataCreate(HealthDataBase):
    pass


class HealthData(HealthDataBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


# ---------- Mood Logs ----------

class MoodLogBase(BaseModel):
    text: str


class MoodLogCreate(MoodLogBase):
    pass


class MoodLog(MoodLogBase):
    id: int
    timestamp: datetime
    sentiment_score: Optional[float] = None

    class Config:
        orm_mode = True


# ---------- Spending Logs ----------

class SpendingLogBase(BaseModel):
    amount: float
    category: Optional[str] = None


class SpendingLogCreate(SpendingLogBase):
    pass


class SpendingLog(SpendingLogBase):
    id: int
    timestamp: datetime
    anomaly_score: Optional[float] = None

    class Config:
        orm_mode = True


# ---------- Risk Score ----------

class RiskScore(BaseModel):
    id: int
    timestamp: datetime
    health_score: float
    mood_score: float
    finance_score: float
    overall_score: float
    level: str
    explanation: str

    class Config:
        orm_mode = True


# ---------- Alert ----------

class Alert(BaseModel):
    id: int
    timestamp: datetime
    message: str
    level: str
    acknowledged: bool

    class Config:
        orm_mode = True