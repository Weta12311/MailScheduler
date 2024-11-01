from mailing.models import Mailing, MailingAttempt
from django.utils import timezone
from datetime import timedelta
import smtplib
from django.core.mail import send_mail
from django.conf import settings


def check_and_send_mailings():
    current_time = timezone.now()

    mailings = Mailing.objects.filter(
        status=Mailing.Status.CREATED, send_time__lte=current_time, is_active=True
    )

    for mailing in mailings:
        if can_send_mailing(mailing):
            send_mailing(mailing)


def can_send_mailing(mailing: Mailing) -> bool:
    last_attempt = (
        MailingAttempt.objects.filter(
            mailing=mailing, status=MailingAttempt.Status.SUCCESS
        )
        .order_by("-attempt_time")
        .first()
    )

    if not last_attempt:
        return True

    frequency_map = {
        Mailing.Frequency.DAILY: timedelta(days=1),
        Mailing.Frequency.WEEKLY: timedelta(weeks=1),
        Mailing.Frequency.MONTHLY: timedelta(days=30),
    }
    next_send_time = last_attempt.attempt_time + frequency_map[mailing.frequency]

    can_send = timezone.now() >= next_send_time
    return can_send


def send_mailing(mailing: Mailing):
    clients = mailing.clients.all()
    emails = [client.email for client in clients]

    attempt_status = MailingAttempt.Status.SUCCESS
    server_response = None

    try:
        mailing.status = Mailing.Status.RUNNING
        mailing.save()

        send_mail(
            subject=mailing.message.title,
            message=mailing.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
        )

        mailing.status = Mailing.Status.CREATED

        if mailing.frequency == Mailing.Frequency.DAILY:
            mailing.send_time += timedelta(days=1)
        elif mailing.frequency == Mailing.Frequency.WEEKLY:
            mailing.send_time += timedelta(weeks=1)
        elif mailing.frequency == Mailing.Frequency.MONTHLY:
            mailing.send_time += timedelta(days=30)

        mailing.save()

    except smtplib.SMTPException as error:
        mailing.is_active = False
        mailing.save()
        attempt_status = MailingAttempt.Status.FAILED
        server_response = str(error)

    finally:
        MailingAttempt.objects.create(
            mailing=mailing, status=attempt_status, server_response=server_response
        )
