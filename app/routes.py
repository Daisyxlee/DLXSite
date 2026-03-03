"""Route handlers for DLX Solution website."""
import html
import os
import re
from email.message import EmailMessage

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for

bp = Blueprint("main", __name__, template_folder="templates")

SUPPORTED_LANGS = {"en", "zh", "es", "fr"}
DEFAULT_LANG = "en"
EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def send_contact_email(from_email: str, subject: str, content: str) -> bool:
    """Send contact form email using Brevo API (HTTPS), not direct SMTP.

    Returns True if sent successfully, False otherwise.

    Configuration (set in .env or environment variables):
    - BREVO_API_KEY           (required)
    - BREVO_FROM_EMAIL        (optional, defaults to CONTACT_TO)
    - BREVO_FROM_NAME         (optional, defaults to "DLX Solution")
    - CONTACT_TO              (defaults to support.dlx@dlxsolution.com)
    """
    api_key = os.environ.get("BREVO_API_KEY")
    to_email = os.environ.get("CONTACT_TO", "support.dlx@dlxsolution.com")
    from_email_cfg = os.environ.get("BREVO_FROM_EMAIL", to_email)
    from_name = os.environ.get("BREVO_FROM_NAME", "DLX Solution")

    if not api_key or not to_email:
        return False

    escaped_content = html.escape(content).replace("\n", "<br>")
    html_body = (
        "<html><body>"
        f"<p><strong>From:</strong> {html.escape(from_email)}</p>"
        f"<p>{escaped_content}</p>"
        "</body></html>"
    )

    payload = {
        "sender": {"name": from_name, "email": from_email_cfg},
        "to": [{"email": to_email}],
        "replyTo": {"email": from_email},
        "subject": f"[DLX Website] {subject}",
        "htmlContent": html_body,
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }

    try:
        resp = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            json=payload,
            headers=headers,
            timeout=10,
        )
        return resp.status_code in (200, 201, 202)
    except Exception:
        return False


def get_lang():
    """Get current language from query param or cookie."""
    return request.args.get("lang") or request.cookies.get("lang", DEFAULT_LANG)


@bp.before_request
def before_request():
    """Set language before each request."""
    lang = get_lang()
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
    from flask import current_app

    current_app._current_lang = lang


@bp.after_request
def set_lang_cookie(response):
    """Persist language preference in cookie when set via query param."""
    lang = request.args.get("lang")
    if lang and lang in SUPPORTED_LANGS:
        response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)
    return response


@bp.route("/")
def home():
    """Home page."""
    return render_template("home.html", active_page="home")


@bp.route("/about")
def about():
    """About page."""
    return render_template("about.html", active_page="about")


@bp.route("/services")
def services():
    """Services page."""
    return render_template("services.html", active_page="services")


@bp.route("/login")
def login():
    """Staff login page — redirects to Zoho Mail. Same layout as main site."""
    return render_template("login.html", active_page="login")


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page with form."""
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        subject = (request.form.get("subject") or "").strip()
        content = (request.form.get("content") or "").strip()

        if not email or not subject or not content:
            flash("error")
            return render_template("contact.html", active_page="contact")

        if not EMAIL_RE.match(email):
            flash("error")
            return render_template("contact.html", active_page="contact")

        from flask import current_app

        try:
            sent = send_contact_email(email, subject, content)
        except Exception:
            current_app.logger.exception("Failed to send contact form email")
            sent = False

        if sent:
            flash("success")
        else:
            flash("send_error")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", active_page="contact")
