from django.db import migrations

def create_default_admin(apps, schema_editor):
    AdminUser = apps.get_model('app', 'AdminUser')
    admin = AdminUser(username='user', password='user')
    admin.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_adminuser'),
    ]

    operations = [
        migrations.RunPython(create_default_admin),
    ]