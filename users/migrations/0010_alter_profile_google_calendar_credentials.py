# Generated by Django 5.0.1 on 2024-01-27 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_google_calendar_credentials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='google_calendar_credentials',
            field=models.TextField(blank=True, null=True),
        ),
    ]
