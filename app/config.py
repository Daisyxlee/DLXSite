"""Application configuration and constants."""
import os

SUPPORTED_LANGS = {"en", "zh", "es", "fr"}
DEFAULT_LANG = "en"

SOCIAL_LINKS = [
    {"url": "https://x.com/DlxSolution", "label": "DLX Solution LLC on X (Twitter)", "icon": "x", "short": "X"},
    {"url": "https://youtube.com/@dlxsolution", "label": "DLX Solution LLC on YouTube", "icon": "youtube", "short": "YT"},
    {"url": "https://www.facebook.com/DLXSolution/", "label": "DLX Solution LLC on Facebook", "icon": "facebook", "short": "f"},
    {"url": "https://www.instagram.com/dlxsolution/", "label": "DLX Solution LLC on Instagram", "icon": "instagram", "short": "IG"},
    {"url": "https://www.linkedin.com/company/dlx-solution/", "label": "DLX Solution LLC on LinkedIn", "icon": "linkedin", "short": "in"},
    {"url": "https://www.facebook.com/groups/dlxsolutioncommunity", "label": "DLX Solution LLC Community on Facebook", "icon": "facebook-group", "short": "G"},
]


def get_config():
    """Return Flask config dict from environment."""
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    return {
        "SECRET_KEY": os.environ.get("SECRET_KEY", "dev-secret-key"),
        "DEBUG": debug,
        "TESTING": False,
    }
