from django.core.mail import send_mail


def send_confirmation_code(email: str, confirmation_code: str) -> None:
    """Отправка кода подтверждения по электронной почте."""
    subject: str = 'Код подтверждения регистрации в YaMDB'
    message: str = f'Ваш код подтверждения: {confirmation_code}'
    from_email: str = 'yamdb@gmail.com'
    recipient_list: list[str] = [email]
    send_mail(subject, message, from_email, recipient_list)
