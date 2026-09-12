from app.extensions import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

class IncomingWebhook(db.Model):
    __tablename__ = "incoming_webhooks"

    id = db.Column(db.Integer, primary_key = True)
    source = db.Column(db.String(50), nullable = False)
    source_id = db.Column(db.String(255), nullable = False)
    payload = db.Column(JSONB, nullable = False)
    received_at = db.Column(db.DateTime,server_default = func.now() , nullable = False)
    #status will be active at start of a webhook and will be taken to delivered and dead_letter accordingly to how the next processes goes
    status = db.Column(db.Enum('active', 'delivered', 'dead_letter', name = 'webhook_status'),
                       nullable = False,
                       default = 'active')
    __table_args__ = (
        db.UniqueConstraint(
            "source",
            "source_id",
            name = "uq_incoming_webhook_source_source_id",
        ),
    )

class Destination(db.Model):
    __tablename__ = "destination"

    id = db.Column(db.Integer,primary_key = True)
    source = db.Column(db.String(50), nullable = False, unique = True)
    url = db.Column(db.String(255), nullable = False)
    secret_token = db.Column(db.String(255), nullable = False)

class RetryAttempt(db.Model):
    __tablename__ = "retry_attempt"

    id = db.Column(db.Integer, primary_key = True)
    incoming_webhook_id = db.Column(db.Integer, db.ForeignKey('incoming_webhooks.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    attempt_number = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Enum('pending', 'processing', 'delivered', 'failed', name = 'attempt_status'),
                       nullable = False,
                       default = 'pending')
    responce_code = db.Column(db.String(255))
    responce_message = db.Column(db.String(255))
    error_message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default = func.now())
    next_retry_at = db.Column(db.DateTime)

    __table_args__ = (
            db.Index(
                'ix_retry_attempt_status_next_retry_at', 'status', 'next_retry_at'
            ),)