# Generated by Django 3.2 on 2022-03-18 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('undangan', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='undangan',
            old_name='type',
            new_name='undangan_type',
        ),
    ]