import uuid
import string
import secrets

def generate_id(length=8):
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def handler(request):
    return {
        "status": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": {
            "full_uuid": str(uuid.uuid4()),
            "short_id": generate_id(6),
            "message": "Ваш ID сгенерирован!"
        }
    }

