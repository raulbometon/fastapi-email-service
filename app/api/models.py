# app/api/models.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional

class EmailRequest(BaseModel):
    to: List[EmailStr]
    template: str
    language_code: str = Field(default='en')
    title_variables: Optional[Dict[str, str]] = None
    variables: Optional[Dict[str, str]] = None
    from_alias: Optional[EmailStr] = None
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None
    reply_to: Optional[EmailStr] = None

