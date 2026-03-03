# Deploy DLX Solution to https://dlxsolution.com

This guide walks you through deploying the Flask site to your domain. Choose one option below.

---

## Option 1: Render (recommended — free tier)

1. **Sign up** at [render.com](https://render.com) and connect your GitHub.
2. **Create a Web Service** → Connect your repo (or push `DLXSite` to GitHub first).
3. **Configure:**
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:app`
4. **Environment variables** (in Render dashboard → Environment):
   - `SECRET_KEY` — generate a random string (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `FLASK_DEBUG` — `0`
   - `CONTACT_TO` — `support.dlx@dlxsolution.com`
   - Add SMTP vars if you want the contact form to work: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
5. **Custom domain:** Render dashboard → Your service → Settings → Custom Domains → Add `dlxsolution.com` and `www.dlxsolution.com`.
6. **DNS:** In your domain registrar (where you bought dlxsolution.com), add:
   - **A record** `@` → Render’s IP (Render shows this when you add the domain)
   - **CNAME** `www` → `your-app.onrender.com`

Render will provision HTTPS automatically.

---

## Option 2: Railway

1. Sign up at [railway.app](https://railway.app) and connect GitHub.
2. **New Project** → Deploy from GitHub → select your repo.
3. Railway detects the Procfile; no extra config needed.
4. **Variables:** Project → Variables → Add:
   - `SECRET_KEY`, `FLASK_DEBUG=0`, `CONTACT_TO`, and SMTP vars
5. **Custom domain:** Settings → Add domain `dlxsolution.com`, then configure DNS per Railway’s instructions.

---

## Option 3: PythonAnywhere

1. Create an account at [pythonanywhere.com](https://www.pythonanywhere.com).
2. **Upload** your project (or connect via Git) to your home directory.
3. **Create a Web app** → Flask → point to your app folder and `wsgi.py`.
4. **Virtualenv:** Add your project path and run `pip install -r requirements.txt`.
5. **Static files:** Map `/static/` to `app/static/`.
6. **Custom domain:** In the Web tab, add `dlxsolution.com` and follow their DNS instructions.

---

## Option 4: VPS (Nginx + Gunicorn)

If you have a server (DigitalOcean, Linode, etc.):

1. Clone the repo and install dependencies in a virtualenv.
2. Run with Gunicorn behind Nginx (Nginx handles HTTPS with Let’s Encrypt).
3. Use `gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app` and proxy to it from Nginx.

---

## Checklist before going live

- [ ] Set `FLASK_DEBUG=0` (or unset) in production
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure SMTP env vars if you want the contact form to send email
- [ ] Point `dlxsolution.com` and `www.dlxsolution.com` DNS to your host
- [ ] Ensure HTTPS is enabled (most platforms do this automatically)
