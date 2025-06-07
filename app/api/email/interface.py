# app/api/email/interface.py

from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import EmailStr

class IMailer(ABC):
    @abstractmethod
    def send(
        self,
        to: List[EmailStr],
        subject: str,
        html_body: str,
        from_alias: Optional[EmailStr],
        cc: Optional[List[EmailStr]],
        bcc: Optional[List[EmailStr]],
        reply_to: Optional[EmailStr]
    ) -> str:
        ...