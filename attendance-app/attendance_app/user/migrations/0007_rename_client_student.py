# Generated by Django 4.2.2 on 2023-06-27 02:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0006_delete_division_alter_course_teacher_id'),
        ('user', '0006_division_alter_client_birth_date_alter_client_gender_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Client',
            new_name='Student',
        ),
    ]