# Generated by Django 4.2.2 on 2023-06-28 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_course_end_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='classattend',
            name='attend_state',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='classattend',
            name='end_at',
            field=models.TimeField(default=None),
        ),
    ]