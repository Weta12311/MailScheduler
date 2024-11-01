from apscheduler.schedulers.background import BackgroundScheduler

from mailing.services.mailing_service import check_and_send_mailings


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_mailings, "interval", minutes=1)
    scheduler.start()
