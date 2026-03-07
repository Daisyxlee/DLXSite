# DLX Solution

https://dlxsolution.com — Design. Lead. Transform.

## Local development

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env     # Edit .env, set FLASK_DEBUG=1
python run.py
```

Open http://127.0.0.1:5000

## Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for Render, Railway, or VPS.
