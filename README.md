# Webhook Relay

Receive GitHub webhooks, verify HMAC signatures, and store them for relay/retry.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
docker compose up -d db
flask --app run db upgrade  # or: alembic upgrade head
python run.py
```
