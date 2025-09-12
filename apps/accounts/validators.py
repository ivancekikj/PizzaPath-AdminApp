import re

from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):  # At least one uppercase letter
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):  # At least one lowercase letter
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):  # At least one digit
            raise ValidationError("Password must contain at least one digit.")

    def get_help_text(self):
        return (
            "Your password must be at least 8 characters long and include at least one uppercase letter, one "
            "lowercase letter, and one number."
        )
