# TODO: core.utils.models
from django.db import models

# TODO: core.utils.models.ModelManager
class ModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)