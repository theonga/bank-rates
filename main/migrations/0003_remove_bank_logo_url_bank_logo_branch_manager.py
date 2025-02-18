# Generated by Django 5.1.6 on 2025-02-09 13:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='logo_url',
        ),
        migrations.AddField(
            model_name='bank',
            name='logo',
            field=models.ImageField(default='', upload_to='logos/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branch',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_branches', to=settings.AUTH_USER_MODEL),
        ),
    ]
