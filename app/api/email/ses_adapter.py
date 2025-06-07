# app/api/email/ses_adapter.py

from typing import List, Optional
from pydantic import EmailStr
from app.api.email.interface import IMailer
from app.config import settings
import boto3
from botocore.exceptions import ClientError

class SESMailer(IMailer):
    def __init__ (self):
        self.client = boto3.client(
            "ses",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_default_region
        )
        self.default_from = settings.default_from

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
        
        source = str(from_alias) if from_alias else self.default_from
        destination = {"ToAddresses": [str(addr) for addr in to]}

        if cc:
            destination["CcAddresses"] = [str(addr) for addr in cc]
        if bcc:
            destination["BccAddresses"] = [str(addr) for addr in bcc]

        message = {
            "Subject": {"Data": subject},
            "Body": {"Html": {"Data": html_body}},
        }

        params = {
            "Source": source,
            "Destination": destination,
            "Message": message,
        }
        
        if reply_to:
            params["ReplyToAddresses"] = [str(reply_to)]

        try:
            resp = self.client.send_email(**params)
            return resp["MessageId"]
        
        except ClientError as e:
            raise RuntimeError(f"SES error: {e.response['Error']['Message']}") from e
        