# Generated by Django 5.0.1 on 2024-01-19 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('1', 'Mental Health'), ('2', 'Heart Disease'), ('3', 'Covid19'), ('4', 'Immunization'), ('5', 'Others')], max_length=20),
        ),
    ]