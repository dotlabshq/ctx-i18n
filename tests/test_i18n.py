import pytest
import asyncio
from pathlib import Path
import os

from ctx_i18n import _, set_locale, load_translations

@pytest.fixture
def locales_path() -> Path:
    """Fixture to provide the path to the test locales directory."""
    return Path(__file__).parent / "locales"

def test_load_translations_direct(locales_path: Path):
    """Tests loading a specific translation file."""
    translations = load_translations("tr", base_path=locales_path.parent)
    assert translations["greeting"] == "Merhaba"

def test_load_translations_fallback_to_en(locales_path: Path):
    """Tests that it falls back to 'en' if the locale file doesn't exist."""
    translations = load_translations("fr", base_path=locales_path.parent) # 'fr' does not exist
    assert translations["greeting"] == "Hello"

def test_load_translations_file_not_found(tmp_path: Path):
    """Tests that a FileNotFoundError is raised if no translation files can be found."""
    with pytest.raises(FileNotFoundError):
        # This path does not contain a 'locales' directory
        load_translations("fr", base_path=tmp_path)

def test_set_locale_and_translate(locales_path: Path):
    """Tests setting the locale and performing translations."""
    # Set APP_PATH so load_translations can find the locales directory
    os.environ["APP_PATH"] = str(locales_path.parent)

    set_locale("tr")
    assert _("greeting") == "Merhaba"
    assert _("messages.welcome", name="Test") == "Hoşgeldin, Test!"

    set_locale("en")
    assert _("greeting") == "Hello"
    assert _("messages.welcome", name="Test") == "Welcome, Test!"

    # Clean up environment variable
    del os.environ["APP_PATH"]

@pytest.mark.asyncio
async def test_asyncio_context_isolation(locales_path: Path):
    """
    Tests that the locale is isolated between different asyncio tasks,
    demonstrating the power of ContextVar.
    """
    os.environ["APP_PATH"] = str(locales_path.parent)

    async def task_tr():
        set_locale("tr")
        await asyncio.sleep(0.01) # Yield control to allow other tasks to run
        assert _("greeting") == "Merhaba"

    async def task_en():
        set_locale("en")
        await asyncio.sleep(0.01)
        assert _("greeting") == "Hello"

    # Run tasks concurrently
    await asyncio.gather(task_tr(), task_en())

    # The context of the current task should be unaffected
    set_locale("en") # Set a default for the current context
    assert _("greeting") == "Hello" # Assuming default or last set in this context

    del os.environ["APP_PATH"]

def test_translation_with_missing_key(locales_path: Path):
    """Tests that if a translation key is missing, the key itself is returned."""
    os.environ["APP_PATH"] = str(locales_path.parent)
    set_locale("en")
    assert _("non.existent.key") == "non.existent.key"
    del os.environ["APP_PATH"]

def test_load_translations_with_app_path_env(locales_path: Path):
    """Tests that load_translations correctly uses the APP_PATH environment variable."""
    os.environ["APP_PATH"] = str(locales_path.parent)
    
    # load_translations is called inside set_locale
    set_locale("tr")
    assert _("greeting") == "Merhaba"

    del os.environ["APP_PATH"]
