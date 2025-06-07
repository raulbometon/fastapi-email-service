# app/api/controllers.py

from app.api.email.interface import IMailer
from app.api.email.ses_adapter import SESMailer
from app.api.models import EmailRequest
from app.api.email.types import email_test_builder, email_test_with_vars_builder
from app.config import settings

TYPE_BUILDERS = {
    "test_email": email_test_builder.build_email,
    "test_email_with_vars": email_test_with_vars_builder.build_email
}

def _get_mailer() -> IMailer:

    if settings.default_mailer == "ses":
        return SESMailer()
    else:
        return SESMailer()
    

async def send_email(emailInfo: EmailRequest):
    template_type = emailInfo.template
    language = emailInfo.language_code
    title_variables = emailInfo.title_variables
    variables = emailInfo.variables

    builder_func = TYPE_BUILDERS.get(template_type)

    if builder_func is None:
        return{
            "status": "error",
            "message": f"Template {template_type} does not exist"
        }
    
    mailer: IMailer = _get_mailer()
    
    try:
        subject, html_body = await builder_func(language, title_variables, variables)

        message_id = mailer.send(
            to=emailInfo.to,
            subject=subject,
            html_body=html_body,
            from_alias=emailInfo.from_alias,
            cc=emailInfo.cc,
            bcc=emailInfo.bcc,
            reply_to=emailInfo.reply_to
        )
        
        return{
            "status": "sent",
            "message_id": message_id
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
