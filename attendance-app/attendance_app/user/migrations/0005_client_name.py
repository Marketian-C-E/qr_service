# Generated by Django 4.2.2 on 2023-06-24 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_rename_user_client"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="name",
            field=models.CharField(default="unknown", max_length=10),
            preserve_default=False,
        ),
    ]