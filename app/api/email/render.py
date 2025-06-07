# app/api/email/render.py
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.config import settings

env_jinja2 = Environment(
    loader=FileSystemLoader(settings.templates_dir),
    autoescape=select_autoescape(["html", "xml"])
)

def render_template(template_name: str, language: str, variables: dict) -> str:

    template_path = f"{language}/{template_name}.html"

    template = env_jinja2.get_or_select_template(template_path)

    context = variables or {}
    return template.render(**context)