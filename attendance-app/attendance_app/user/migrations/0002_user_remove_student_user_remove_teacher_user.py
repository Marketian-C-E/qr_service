# Generated by Django 4.2.2 on 2023-06-24 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("birth_date", models.CharField(max_length=6)),
                ("gender", models.CharField(max_length=10)),
                ("division", models.CharField(max_length=30)),
                ("qr_code", models.ImageField(upload_to="qr_student/")),
            ],
        ),
        migrations.RemoveField(model_name="student", name="user",),
        migrations.RemoveField(model_name="teacher", name="user",),
    ]