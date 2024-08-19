from email_validator import validate_email, EmailNotValidError


def email_validator(email: str) -> str:
    try:
        validate_email(email)
    except:
        raise ValueError("Email inválido.")

    return email
