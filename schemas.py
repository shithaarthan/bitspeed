# schemas.py

from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Pydantic Models for Data Validation ---

# Model for the incoming request body JSON
class IdentifyRequest(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None

# Model for the nested "contact" object in the response
class ContactData(BaseModel):
    primaryContatctId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[int]

# Model for the final, top-level JSON response
class IdentifyResponse(BaseModel):
    contact: ContactData