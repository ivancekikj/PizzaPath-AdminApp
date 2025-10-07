import requests
from django.conf import settings
from requests import Response

email_app_url = settings.EMAIL_APP_URL
customer_app_url = settings.CUSTOMER_APP_URL


def send_email_confirmation_link(email: str, token: str) -> bool:
    if not email_app_url:
        return True
    body = {"email": email, "confirm_link": f"{customer_app_url}/account/confirm?token={token}"}
    response: Response = requests.post(f"{email_app_url}/api/email-confirmation", json=body)
    return response.ok
