# Generated by Django 5.1.3 on 2024-11-26 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_default_admin'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdminUser',
        ),
    ]
