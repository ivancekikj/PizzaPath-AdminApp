import requests
from django.conf import settings
from requests import Response

email_app_url = settings.EMAIL_APP_URL


def send_email_confirmation_link(email: str, confirm_link: str) -> bool:
    if not email_app_url:
        return True

    url = f"{email_app_url}/api/email-confirmation"
    body = {"email": email, "confirm_link": confirm_link}
    response: Response = requests.post(url, json=body)
    return response.ok
