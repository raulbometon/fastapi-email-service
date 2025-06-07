# app/api/email/i18n.py
import json
import os
from functools import lru_cache
from typing import Any, Dict, Optional

BASE_LOCALES_PATH = os.path.join(os.path.dirname(__file__), "../../locales")

@lru_cache(maxsize=None)
def load_translations(language: str) -> Dict[str, str]:
    file_path = os.path.join(BASE_LOCALES_PATH, f"{language}.json")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"i18n json file not found for '{language}'")
    with open(file_path, "r", encoding="utf-8") as f:
        data: Dict[str, str] = json.load(f)
    return data

def get_subject(template_name: str, language: str, **kwargs: Any) -> str:

    try:
        translations = load_translations(language)
    except FileNotFoundError:
        translations = load_translations("en")

    if template_name not in translations:
        raise KeyError(f"Key'{template_name}' does not exist in {language}.json")

    template_str = translations[template_name]
    if kwargs:
        try:
            return template_str.format(**kwargs)
        except KeyError as e:
            raise KeyError(f"Varible {e} is needed to format the subject") from e
    return template_str