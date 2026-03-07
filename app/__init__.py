"""DLX Solution website application."""
import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask

from app.config import SOCIAL_LINKS, get_config

TRANSLATIONS = {}


def load_translations():
    """Load all translation JSON files into TRANSLATIONS."""
    global TRANSLATIONS
    trans_dir = Path(__file__).parent / "translations"
    for path in trans_dir.glob("*.json"):
        lang = path.stem
        with open(path, encoding="utf-8") as f:
            TRANSLATIONS[lang] = json.load(f)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.update(get_config())
    load_translations()

    @app.context_processor
    def inject_globals():
        def t(key, default=""):
            try:
                parts = key.split(".")
                from flask import current_app

                lang = getattr(current_app, "_current_lang", "en")
                data = TRANSLATIONS.get(lang) or TRANSLATIONS.get("en") or {}
                for part in parts:
                    if isinstance(data, dict) and part in data:
                        data = data[part]
                    else:
                        return default or ""
                result = data if isinstance(data, str) else default
                return result if result is not None else ""
            except Exception:
                return default or ""

        return {
            "t": t,
            "now": lambda: datetime.now(timezone.utc),
            "social_links": SOCIAL_LINKS,
        }

    from app.routes import bp

    app.register_blueprint(bp)

    return app


app = create_app()
