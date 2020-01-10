from django.db import models
from django.contrib.auth.models import BaseUserManager


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomBaseUserManager(CustomModelManager, BaseUserManager):
    pass
