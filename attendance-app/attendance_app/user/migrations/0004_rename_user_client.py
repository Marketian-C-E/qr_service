# Generated by Django 4.2.2 on 2023-06-24 10:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("course", "0002_alter_classattend_student_id_alter_course_teacher_id"),
        ("user", "0003_delete_student_delete_teacher_user_user"),
    ]

    operations = [
        migrations.RenameModel(old_name="User", new_name="Client",),
    ]
