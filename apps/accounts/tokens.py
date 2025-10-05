from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

from apps.accounts.models import Customer

signer = TimestampSigner()


def generate_email_token(user: Customer) -> str:
    value = f"{user.id}:{user.email}"
    return signer.sign(value)


def verify_email_token(token, max_age=86400) -> tuple[int | None, str | None]:
    try:
        value = signer.unsign(token, max_age=max_age)
        user_id, email = value.split(":")
        return int(user_id), email
    except (BadSignature, SignatureExpired):
        return None, None
