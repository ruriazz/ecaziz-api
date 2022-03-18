import datetime
from django.db import models
from core.utils.models import ModelManager
from enums.undangan_type import UndanganType
from applications.users.models import User

# TODO: models.Undangan
class Undangan(models.Model):
    class Meta:
        managed = True
        db_table = 'undangan'

    id = models.AutoField(primary_key=True)
    undangan_type = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in UndanganType])
    person_type = models.CharField(max_length=100, null=True, blank=True)
    person_name = models.CharField(max_length=150, null=False, blank=False)
    person_partner = models.CharField(max_length=100, null=True, blank=True)
    person_location = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    link = models.CharField(max_length=150, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    last_send = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ModelManager()
    default_objects = models.Manager()

    def soft_delete(self):
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()
