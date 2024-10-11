from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Mailing, MailingAttempt
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, "interval", minutes=1)  # Каждый 1 минуту
    scheduler.start()

def send_mailing():
    current_datetime = timezone.now()
    mailings = Mailing.objects.filter(
        start_date__lte=current_datetime, status="running"
    )

    for mailing in mailings:
        # Логика отправки писем
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()],
                fail_silently=False,
            )
            logger.info(f"Рассылка '{mailing.message.subject}' успешно отправлена.")
            # Здесь можно создать запись о попытке рассылки
            MailingAttempt.objects.create(mailing=mailing, status='success', response="Mail sent successfully")
        except Exception as e:
            logger.error(f"Ошибка при отправке рассылки '{mailing.message.subject}': {str(e)}")
            # Создаем запись о неудачной попытке рассылки
            MailingAttempt.objects.create(mailing=mailing, status='failure', response=str(e))
