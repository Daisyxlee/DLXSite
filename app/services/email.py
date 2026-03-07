"""Email service - contact form delivery via Brevo API."""
import html
import os

import requests

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_TIMEOUT = 10


def send_contact_email(from_email: str, subject: str, content: str) -> bool:
    """Send contact form email via Brevo API.

    Returns True if sent successfully, False otherwise.

    Config (env): BREVO_API_KEY (required), BREVO_FROM_EMAIL, BREVO_FROM_NAME, CONTACT_TO.
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
        resp = requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=BREVO_TIMEOUT)
        return resp.status_code in (200, 201, 202)
    except Exception:
        return False
