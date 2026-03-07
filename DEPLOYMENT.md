# Deploy DLX Solution to https://dlxsolution.com

Choose one option below.

---

## Option 1: Render (recommended)

1. **Sign up** at [render.com](https://render.com) and connect your GitHub.
2. **Create a Web Service** → Connect your repo.
3. **Configure:**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:app`
4. **Environment variables:**
   | Variable         | Required | Description                              |
   |------------------|----------|------------------------------------------|
   | `SECRET_KEY`     | Yes      | Random string (see below)                |
   | `FLASK_DEBUG`    | No       | Set to `0` for production                |
   | `CONTACT_TO`     | No       | Default: support.dlx@dlxsolution.com     |
   | `BREVO_API_KEY`  | Yes*     | Required for contact form to send email  |
   | `BREVO_FROM_EMAIL` | No     | Sender email (default: CONTACT_TO)       |
   | `BREVO_FROM_NAME`  | No     | Sender name (default: DLX Solution)      |

   Generate SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`

5. **Custom domain:** Settings → Custom Domains → Add `dlxsolution.com`, `www.dlxsolution.com`.
6. **DNS:** Add A record and CNAME per Render's instructions.

---

## Option 2: Railway

1. Sign up at [railway.app](https://railway.app), connect GitHub.
2. New Project → Deploy from GitHub.
3. **Variables:** Add `SECRET_KEY`, `FLASK_DEBUG=0`, `BREVO_API_KEY`, `CONTACT_TO`.
4. **Custom domain:** Settings → Add domain, configure DNS.

---

## Option 3: VPS (Nginx + Gunicorn)

1. Clone repo, create virtualenv, `pip install -r requirements.txt`.
2. Run: `gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app`
3. Proxy with Nginx; use Certbot for HTTPS.

---

## Pre-deploy checklist

- [ ] Set `FLASK_DEBUG=0` in production
- [ ] Set strong `SECRET_KEY`
- [ ] Add `BREVO_API_KEY` for contact form
- [ ] Configure DNS for your domain
- [ ] Verify HTTPS is enabled
