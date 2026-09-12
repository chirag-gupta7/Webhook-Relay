import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://admin:1234@localhost:5432/Webhook_relay",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
