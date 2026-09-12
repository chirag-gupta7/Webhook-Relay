import json
from flask import Blueprint, request
from app.extensions import db
from app.models import Destination, IncomingWebhook
from app.security import verify_signature

webhooks_bp = Blueprint('webhooks', __name__)

@webhooks_bp.route('/webhooks/<source>', methods = ['POST'])
def receive_webhook(source):
    raw_body = request.get_data()

    destination = Destination.query.filter_by(source = source).first()

    if not destination:
        return f"source {source} is not configured", 404

    signature_header_value = request.headers.get('X-Hub-Signature-256')

    if not signature_header_value:
        return "No Signature received", 401

    if not verify_signature(destination.secret_token, raw_body, signature_header_value):
        return "Invalid Signature", 401

    source_id = request.headers.get('X-Github-Delivery')

    source_id_already_existing = IncomingWebhook.query.filter_by(source = source, source_id = source_id).first()

    if source_id_already_existing:
        return "Webhook already received", 200

    payload = json.loads(raw_body)

    new_webhook = IncomingWebhook(
        source = source,
        source_id = source_id,
        payload = payload
    )
    db.session.add(new_webhook)
    db.session.commit()

    return f"received from {source}", 200