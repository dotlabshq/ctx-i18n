# NOTE: This example will not run on Python 3.14 due to an incompatibility
# between FastAPI's dependencies (pydantic-core, watchfiles) and Python 3.14.
# This file is provided for future reference.

from fastapi import FastAPI, Request, Header
from typing import Optional
from pathlib import Path
import os

from ctx_i18n import _, set_locale

app = FastAPI()

# Set the APP_PATH environment variable for load_translations
os.environ["APP_PATH"] = str(Path(__file__).parent)

@app.middleware("http")
async def set_language_middleware(request: Request, call_next):
    lang = request.query_params.get("lang") or request.headers.get("Accept-Language", "en").split(',')[0].split('-')[0]
    set_locale(lang)
    response = await call_next(request)
    return response

@app.get("/")
def index(name: Optional[str] = "Guest"):
    return {
        "app_name": _("app_name"),
        "welcome_message": _("welcome_message", name=name),
        "current_language": _("current_language"),
    }

# To run this example (on a compatible Python version):
# uvicorn main_fastapi:app --reload
