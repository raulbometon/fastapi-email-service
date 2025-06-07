# api/email/types/email_test_with_vars_builder.py
from typing import Dict, Optional, Tuple

from app.api.email.i18n import get_subject
from app.api.email.render import render_template

async def build_email(language: str, title_variables: Optional[Dict[str, str]],variables: Optional[Dict[str, str]]) -> Tuple[str, str]:
    subject = get_subject("test_email_with_vars", language, **(title_variables or {}))

    ctx = variables or {}
    html_body = render_template("test_email_with_vars", language, ctx)

    return subject, html_body
