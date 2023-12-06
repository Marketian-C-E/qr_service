# Generated by Django 4.2.2 on 2023-06-23 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Survey",
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
                ("question_num", models.IntegerField()),
                ("question", models.CharField(max_length=100)),
                (
                    "course_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.course"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SurveyReply",
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
                ("reply_num", models.IntegerField()),
                ("reply", models.TextField()),
                (
                    "survey_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="survey.survey"
                    ),
                ),
            ],
        ),
    ]
