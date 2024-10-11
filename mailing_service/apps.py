from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MailingServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing_service"

    def ready(self):
        from .tasks import start  # Импортируем здесь, чтобы избежать ошибок

        def start_scheduler(sender, **kwargs):
            start()  # Запускаем задачи планировщика без задержки

        post_migrate.connect(start_scheduler, sender=self)
