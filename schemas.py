# schemas.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Pydantic Models for Data Validation ---

# Model for the incoming request body JSON.
# FastAPI will use this to automatically validate that:
# - email, if provided, is a valid email format.
# - phoneNumber, if provided, is a string.
# - The fields are optional.
class IdentifyRequest(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None

# Model for the nested "contact" object in the response.
class ContactData(BaseModel):
    primaryContatctId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

# Model for the final, top-level JSON response.
# FastAPI uses this with 'response_model' to ensure our API
# always returns data in this exact structure.
class IdentifyResponse(BaseModel):
    contact: ContactData