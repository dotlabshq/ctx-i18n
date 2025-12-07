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

### 2. Set Environment Variable

Set the `APP_PATH` environment variable to the directory containing your `locales` folder.

### 3. Use in your code

```python
import os
from pathlib import Path
from ctx_i18n import set_locale, _

# Set the APP_PATH to the directory containing the 'locales' folder.
os.environ["APP_PATH"] = str(Path.cwd())

# Set the locale to Turkish
set_locale("tr")
print(_("greeting", name="World"))  # Output: Merhaba, World!

# Set the locale to English
set_locale("en")
print(_("greeting", name="World"))  # Output: Hello, World!
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
