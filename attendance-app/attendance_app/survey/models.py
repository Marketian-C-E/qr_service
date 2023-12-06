from django.db import models
from course.models import Course
from user.models import Student
from django.shortcuts import get_object_or_404

# Create your models here.
#설문 양식
class Survey(models.Model):
    course_id = models.OneToOneField(Course, on_delete=models.CASCADE)
    question1 = models.CharField(max_length=200)
    question2 = models.CharField(max_length=200, blank=True)
    question3 = models.CharField(max_length=200, blank=True)
    question4 = models.CharField(max_length=200, blank=True)
    question5 = models.CharField(max_length=200, blank=True)
    question6 = models.CharField(max_length=200, blank=True)
    question7 = models.CharField(max_length=200, blank=True)
    question8 = models.CharField(max_length=200, blank=True)
    question9 = models.CharField(max_length=200, blank=True)
    question10 = models.CharField(max_length=200, blank=True)
    question11 = models.CharField(max_length=200, blank=True)
    question12 = models.CharField(max_length=200, blank=True)
    question13 = models.CharField(max_length=200, blank=True)
    question14 = models.CharField(max_length=200, blank=True)
    question15 = models.CharField(max_length=200, blank=True)

    def __str__(self):
        course = get_object_or_404(Course, pk=self.course_id.pk)
        return f'[{course.course_name}] 설문지 양식'


# 설문 답변
class SurveyReply(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default=0)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    reply1 = models.TextField()
    reply2 = models.TextField(blank=True)
    reply3 = models.TextField(blank=True)
    reply4 = models.TextField(blank=True)
    reply5 = models.TextField(blank=True)
    reply6 = models.TextField(blank=True)
    reply7 = models.TextField(blank=True)
    reply8 = models.TextField(blank=True)
    reply9 = models.TextField(blank=True)
    reply10 = models.TextField(blank=True)
    reply11 = models.TextField(blank=True)
    reply12 = models.TextField(blank=True)
    reply13 = models.TextField(blank=True)
    reply14 = models.TextField(blank=True)
    reply15 = models.TextField(blank=True)

    submit_survey = models.BooleanField(default=False)

    def __str__(self):
        survey = get_object_or_404(Survey, pk=self.survey_id.pk)
        course = get_object_or_404(Course, pk=survey.course_id.pk)
        return f'[{course.course_name}] 설문지 답변 - {self.pk}'
