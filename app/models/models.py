from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

# Helper for MongoDB ObjectId with Pydantic validation
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# User Schema
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    phone: str
    name: str
    email: Optional[EmailStr] = None
    preferences: Optional[Dict[str, Any]] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# Activity sub-document schema inside Trip.activities
class Activity(BaseModel):
    activityId: PyObjectId = Field(default_factory=PyObjectId)
    title: str
    description: Optional[str] = None
    dateTime: Optional[datetime] = None
    location: Optional[Dict[str, Any]] = None  # e.g., {"address": str, "lat": float, "lng": float}

    class Config:
        json_encoders = {ObjectId: str}

# SharedWith sub-document schema inside Trip.sharedWith
class SharedWith(BaseModel):
    phone: str
    permissions: str  # "view" or "edit"

# Trip Schema
class Trip(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    ownerPhone: str
    title: str
    destinations: List[str]
    startDate: datetime
    endDate: datetime
    budget: Optional[float] = None
    activities: Optional[List[Activity]] = []
    bookings: Optional[List[PyObjectId]] = []
    sharedWith: Optional[List[SharedWith]] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# Booking Schema
class Booking(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    tripId: PyObjectId
    userPhone: str
    bookingType: str  # e.g., "flight", "hotel"
    details: Dict[str, Any]
    status: str  # "pending", "confirmed", "cancelled"
    paymentStatus: str  # "paid", "failed", "pending"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# Collaboration / Comment Schema
class CollaborationComment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    tripId: PyObjectId
    userPhone: str
    comment: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
