# Generated by Django 4.2.2 on 2023-06-26 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_rename_division_name_course_division_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='division_id',
        ),
        migrations.AddField(
            model_name='course',
            name='division_name',
            field=models.CharField(default='unknown', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
