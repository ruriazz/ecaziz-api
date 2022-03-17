# Generated by Django 3.2 on 2022-03-17 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('undangan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ucapan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sender', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True)),
                ('undangan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='undangan.undangan')),
            ],
            options={
                'db_table': 'ucapan',
                'managed': True,
            },
        ),
    ]
