import smtplib

from django.core.mail import send_mail
from django.core.management import BaseCommand
from mailing.models import Mailing, MailingAttempt
from mailscheduler import settings


class Command(BaseCommand):
    help = "Send an immediate mailing"

    def handle(self, *args, **options):
        while True:
            mailings = Mailing.objects.filter(status=Mailing.Status.CREATED)

            if not mailings:
                print("Нет доступных рассылок для отправки.")
                return

            print("\nДоступные рассылки:")
            print(
                f"{'Номер рассылки':<15} {'Номер сообщения':<20} {'Количество клиентов':<25}"
            )
            for mailing in mailings:
                print(
                    f"{mailing.id:<15} {mailing.message.id:<20} {mailing.clients.count():<25}"
                )

            print("\nВведите номер рассылки для отправки или 'q' для выхода:")
            user_input = input()

            if user_input.lower() == "q":
                print("Выход из программы.")
                break

            if user_input.isdigit():
                mailing_id = int(user_input)
                if Mailing.objects.filter(pk=mailing_id).exists():
                    mailing = Mailing.objects.get(pk=mailing_id)
                    single_mailing(mailing)
                    print(f"Рассылка {mailing.id} запущена.")
                    break
                else:
                    print("Такой рассылки не существует.")
            else:
                print(
                    "Пожалуйста, введите правильный номер рассылки или 'q' для выхода."
                )


def single_mailing(mailing):
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

    except smtplib.SMTPException as error:
        mailing.is_active = False
        mailing.save()
        attempt_status = MailingAttempt.Status.FAILED
        server_response = str(error)

    finally:
        MailingAttempt.objects.create(
            mailing=mailing, status=attempt_status, server_response=server_response
        )
