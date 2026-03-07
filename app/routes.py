"""Route handlers for DLX Solution website."""
import re

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app.config import DEFAULT_LANG, SUPPORTED_LANGS
from app.services.email import send_contact_email

bp = Blueprint("main", __name__, template_folder="templates")

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def get_lang():
    """Current language from query param or cookie."""
    return request.args.get("lang") or request.cookies.get("lang", DEFAULT_LANG)


@bp.before_request
def before_request():
    """Set language before each request."""
    lang = get_lang()
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG
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
    return render_template("home.html", active_page="home")


@bp.route("/about")
def about():
    return render_template("about.html", active_page="about")


@bp.route("/services")
def services():
    return render_template("services.html", active_page="services")


@bp.route("/login")
def login():
    return render_template("login.html", active_page="login")


@bp.route("/contact", methods=["GET", "POST"])
def contact():
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

        try:
            sent = send_contact_email(email, subject, content)
        except Exception:
            current_app.logger.exception("Failed to send contact form email")
            sent = False

        flash("success" if sent else "send_error")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", active_page="contact")
