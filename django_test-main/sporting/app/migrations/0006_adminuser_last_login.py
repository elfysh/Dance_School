# Generated by Django 5.1.3 on 2024-11-26 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_add_default_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
