from django.db import models

from core.utils.models import ModelManager

# TODO: models.User
class User(models.Model):
    class Meta:
        managed = True
        db_table = 'user'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ModelManager()
    default_objects = models.Manager()

# TODO: models.AuthenticationAttempt
class AuthenticationAttempt(models.Model):
    class Meta:
        managed = True
        db_table = 'authentication_attempt'

    id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=20)
    user_agent = models.CharField(max_length=256, null=True, blank=True)
    count = models.SmallIntegerField(default=1)
    attempt_at = models.DateTimeField(auto_now=True)

# TODO: models.AuthenticatedUser
class AuthenticatedUser(models.Model):
    class Meta:
        managed = True
        db_table = 'authenticated_user'

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=256)
    authenticated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)    