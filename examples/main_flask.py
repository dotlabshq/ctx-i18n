from flask import Flask, request, g
from pathlib import Path
import os

from ctx_i18n import _, set_locale

app = Flask(__name__)

# Set the APP_PATH environment variable for load_translations
# The base_path for load_translations should be the directory containing the 'locales' folder.
# In this case, it's the 'examples' directory itself.
os.environ["APP_PATH"] = str(Path(__file__).parent)

@app.before_request
def set_language():
    lang = request.args.get("lang") or request.headers.get("Accept-Language", "en").split(',')[0].split('-')[0]
    set_locale(lang)
    g.locale = lang # Store in Flask's global context for easy access in templates/responses

@app.route("/")
def index():
    name = request.args.get("name", "Guest")
    return f"""
    <h1>{_("app_name")}</h1>
    <p>{_("welcome_message", name=name)}</p>
    <p>{_("current_language")} ({g.locale})</p>
    <p>Try adding ?lang=tr or ?lang=en to the URL, or setting the Accept-Language header.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
