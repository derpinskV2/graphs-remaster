import logging

from django.core.management import BaseCommand
from django.conf import settings


from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(
                username=settings.ADMIN_USERNAME, email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD
            )
        except IntegrityError:
            pass
        except Exception as e:
            logger.exception(f"Failed to create superuser. {e}")
