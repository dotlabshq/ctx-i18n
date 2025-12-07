# ctx-i18n: Context-Aware Internationalization

A simple Python library for internationalization (i18n) that uses `ContextVar` to manage the current language (locale). This makes it thread-safe and suitable for concurrent applications like web servers.

## Features

-   Simple API: `set_locale()` and `_()` are all you need.
-   Thread-safe: Uses `ContextVar` for safe use in concurrent environments.
-   Flexible: Works with any web framework (Flask, FastAPI, etc.) or in simple scripts.
-   YAML-based translations.

## Installation

```bash
pip install ctx-i18n
```

You will also need to install `PyYAML`:

```bash
pip install PyYAML
```

## Usage

### 1. Create Translation Files

Create a `locales` directory in your project and add your YAML translation files.

`locales/en.yml`:
```yaml
greeting: "Hello, {name}!"
farewell: "Goodbye."
```

`locales/tr.yml`:
```yaml
greeting: "Merhaba, {name}!"
farewell: "Hoşçakal."
```

### 2. Specify Locales Path (Environment Variable or Function Parameter)

You can tell `ctx-i18n` where to find your `locales` folder in two ways:

**Option A: Environment Variable (Recommended for applications)**
Set the `APP_PATH` environment variable to the absolute path of the directory that *contains* your `locales` folder.

```bash
export APP_PATH=/path/to/your/project
```

**Option B: `base_path` Parameter (Recommended for scripts or specific contexts)**
Pass the `base_path` argument directly to the `set_locale` function (which internally calls `load_translations`). The `base_path` should be the absolute path of the directory that *contains* your `locales` folder.
```python
from pathlib import Path
from ctx_i18n import set_locale, _

# Assuming 'locales' is a subdirectory of your script's current working directory
project_root = Path.cwd()
set_locale("en", base_path=project_root)
```

### 3. Use in your code

```python
import os
from pathlib import Path
from ctx_i18n import set_locale, _

# --- Option A: Using APP_PATH environment variable ---
# Set the APP_PATH to the directory containing the 'locales' folder.
# This is typically done once at application startup.
os.environ["APP_PATH"] = str(Path.cwd()) # Example: current working directory

# Set the locale to Turkish
set_locale("tr")
print(_("greeting", name="World"))  # Output: Merhaba, World!

# --- Option B: Passing base_path directly to set_locale ---
# This overrides APP_PATH for this specific call.
# Assuming 'locales' is a subdirectory of your script's current working directory
project_root = Path.cwd()
set_locale("en", base_path=project_root)
print(_("greeting", name="World"))  # Output: Hello, World!

# If a translation is not found, the key is returned
print(_("non.existent.key"))      # Output: non.existent.key
```

### Web Framework Example (Flask)

`ctx-i18n` is ideal for web apps. Here's how to use it with Flask.

```python
from flask import Flask, request
from pathlib import Path
import os
from ctx_i18n import set_locale, _

app = Flask(__name__)

# Set APP_PATH to the directory containing the 'locales' folder.
os.environ["APP_PATH"] = str(Path(__file__).parent)

@app.before_request
def set_language_from_request():
    # Set locale from a query param (e.g., /?lang=tr) or header
    lang = request.args.get("lang") or request.headers.get("Accept-Language", "en")
    set_locale(lang.split(',')[0].split('-')[0])

@app.route("/")
def home():
    # The `_` function will automatically use the locale set in the middleware.
    return f"<h1>{_('greeting', name='User')}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
```

### Web Framework Example (FastAPI)

`ctx-i18n` also works seamlessly with FastAPI.

**NOTE:** This example might not run on Python 3.14 due to dependency
incompatibilities (pydantic-core, watchfiles) with PyO3.
It is provided for reference.

```python
from fastapi import FastAPI, Request
from typing import Optional
from pathlib import Path
import os
from ctx_i18n import set_locale, _

app = FastAPI()

# Set APP_PATH to the directory containing the 'locales' folder.
os.environ["APP_PATH"] = str(Path(__file__).parent)

@app.middleware("http")
async def set_language_middleware(request: Request, call_next):
    lang = request.query_params.get("lang") or request.headers.get("Accept-Language", "en").split(',')[0].split('-')[0]
    set_locale(lang)
    response = await call_next(request)
    return response

@app.get("/")
async def home(name: Optional[str] = "User"):
    return {
        "app_name": _("app_name"),
        "welcome_message": _("welcome_message", name=name),
        "current_language": _("current_language"),
    }

# To run this FastAPI example (on a compatible Python version):
# 1. Save it as `app_fastapi.py`.
# 2. Make sure you have a `locales` directory next to it.
# 3. Run `uvicorn app_fastapi:app --reload`.
# 4. Visit http://127.0.0.1:8000/?lang=tr and http://127.0.0.1:8000/?lang=en
```

## Running Tests

To run the tests, first install the development dependencies:

```bash
poetry install --with dev
```

Then run `pytest`:

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License.
