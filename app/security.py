import hmac
import hashlib

def verify_signature(secret: str, raw_body: bytes, received_signature: str) -> bool:
    computed_signature = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    without_prefix_received_signature = received_signature.removeprefix("sha256=")
    
    return hmac.compare_digest(computed_signature, without_prefix_received_signature)