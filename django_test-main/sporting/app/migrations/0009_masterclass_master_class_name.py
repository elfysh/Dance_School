# Generated by Django 5.1.3 on 2024-12-01 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_style_style_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterclass',
            name='master_class_name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
