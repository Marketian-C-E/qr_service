# Generated by Django 4.2.2 on 2023-07-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_alter_classattend_start_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classattend',
            name='attend_state',
            field=models.IntegerField(default=0),
        ),
    ]