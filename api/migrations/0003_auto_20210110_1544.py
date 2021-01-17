# Generated by Django 3.1 on 2021-01-10 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20210110_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='rasponsible',
        ),
        migrations.AddField(
            model_name='task',
            name='responsible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rasponsible', to=settings.AUTH_USER_MODEL),
        ),
    ]
