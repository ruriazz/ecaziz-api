# Generated by Django 3.2 on 2022-03-18 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('undangan', '0002_rename_type_undangan_undangan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='undangan',
            name='link',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='person_location',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='person_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='person_partner',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='undangan',
            name='person_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
