from django.db import models
from core.utils.models import ModelManager

from applications.undangan.models import Undangan

# TODO: models.ucapan
class Ucapan(models.Model):
    class Meta:
        managed = True
        db_table = 'ucapan'

    id = models.AutoField(primary_key=True)
    undangan = models.ForeignKey(Undangan, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True)

    objects = ModelManager()
    default_objects = models.Manager()