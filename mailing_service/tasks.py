from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.conf import settings
import pytz
from datetime import datetime, timedelta
from .models import Mailing, MailingAttempt  # Импортируем модели здесь


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = Mailing.objects.filter(
        start_date__lte=current_datetime, status="running"
    )

    for mailing in mailings:
        last_attempt = (
            MailingAttempt.objects.filter(mailing=mailing)
            .order_by("-timestamp")
            .first()
        )
        if last_attempt:
            if (
                mailing.periodicity == "day"
                and last_attempt.timestamp >= current_datetime - timedelta(days=1)
            ):
                continue
            elif (
                mailing.periodicity == "week"
                and last_attempt.timestamp >= current_datetime - timedelta(weeks=1)
            ):
                continue
            elif (
                mailing.periodicity == "month"
                and last_attempt.timestamp >= current_datetime - timedelta(days=30)
            ):
                continue

        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False,
            )
            mailing.status = "completed"
            mailing.save()
            MailingAttempt.objects.create(
                mailing=mailing, status="success", response="Mail sent successfully"
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing, status="failure", response=str(e)
            )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, "interval", seconds=30)  # Отправка каждые 30 секунд
    scheduler.start()
