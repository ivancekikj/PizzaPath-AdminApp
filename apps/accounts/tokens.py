import secrets

from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

from apps.accounts.models import Customer

signer = TimestampSigner()


def generate_email_token(user: Customer) -> str:
    random_value = secrets.token_hex(16)
    value = f"{user.id}:{random_value}"
    return signer.sign(value)


def verify_email_token(token, max_age=86400) -> tuple[int | None, str | None]:
    try:
        value = signer.unsign(token, max_age=max_age)
        user_id, random_value = value.split(":")
        return int(user_id), random_value
    except (BadSignature, SignatureExpired):
        return None, None
