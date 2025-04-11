from pydantic import BaseModel, Field
from datetime import date

class UserBirthdayRequest(BaseModel):
    dateOfBirth: date = Field(..., description="Date of birth in YYYY-MM-DD")