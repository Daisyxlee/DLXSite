"""Route handlers for DLX Solution website."""
import os
import re
import smtplib
from email.message import EmailMessage

from flask import Blueprint, flash, redirect, render_template, request, url_for

bp = Blueprint("main", __name__, template_folder="templates")

SUPPORTED_LANGS = {"en", "zh", "es", "fr"}
DEFAULT_LANG = "en"
EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def send_contact_email(from_email: str, subject: str, content: str) -> bool:
    """Send contact form email using SMTP settings from environment.

    Returns True if sent successfully, False otherwise.

    SMTP configuration (set in .env or environment variables):
    - SMTP_HOST
    - SMTP_PORT (default 587)
    - SMTP_USER
    - SMTP_PASSWORD
    - SMTP_USE_TLS (\"1\" by default, set to \"0\" to disable)
    - CONTACT_TO (defaults to support.dlx@dlxsolution.com)
    """
    host = os.environ.get("SMTP_HOST")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    to_email = os.environ.get("CONTACT_TO", "support.dlx@dlxsolution.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    use_tls = os.environ.get("SMTP_USE_TLS", "1") != "0"

    if not host or not user or not password or not to_email:
        return False

    msg = EmailMessage()
    msg["Subject"] = f"[DLX Website] {subject}"
    msg["From"] = to_email
    msg["To"] = to_email
    msg["Reply-To"] = from_email

    body = f"From: {from_email}\n\n{content}"
    msg.set_content(body)

    with smtplib.SMTP(host, port) as server:
        if use_tls:
            server.starttls()
        server.login(user, password)
        server.send_message(msg)
    return True


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
