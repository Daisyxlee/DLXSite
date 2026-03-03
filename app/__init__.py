"""DLX Solution website application."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from flask import Flask

# Theme colors: navy (#0a2540) and teal (#20e3d2)
TRANSLATIONS = {}


def load_translations():
    """Load all translation JSON files."""
    global TRANSLATIONS
    trans_dir = Path(__file__).parent / "translations"
    for path in trans_dir.glob("*.json"):
        lang = path.stem
        with open(path, encoding="utf-8") as f:
            TRANSLATIONS[lang] = json.load(f)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    load_translations()

    @app.context_processor
    def inject_t():
        def t(key, default=""):
            parts = key.split(".")
            from flask import current_app

            lang = getattr(current_app, "_current_lang", "en")
            data = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
            for part in parts:
                if isinstance(data, dict) and part in data:
                    data = data[part]
                else:
                    return default
            return data if isinstance(data, str) else default

        return dict(t=t, now=lambda: datetime.now(timezone.utc))

    @app.template_filter("replace_lang")
    def replace_lang_filter(url, lang):
        """Replace or add lang query param in URL."""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        params["lang"] = [lang]
        new_query = urlencode(params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))

    from app.routes import bp

    app.register_blueprint(bp)

    return app


app = create_app()
