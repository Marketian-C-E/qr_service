# Generated by Django 4.2.2 on 2023-06-28 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_course_division_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='teacher_id',
            new_name='teacher_name',
        ),
    ]
