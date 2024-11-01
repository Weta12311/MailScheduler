from django.core.mail import send_mail

from mailscheduler.settings import EMAIL_HOST_USER


def send_email_confirm(url, email):
    send_mail(
        subject="Подтвержение регистрации на сайте Планировщика рассылок",
        message=f"Для подтверждения регистрации, перейдите по ссылке {url}",
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
    )
