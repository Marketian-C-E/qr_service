from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
class Student(models.Model):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
        ('O', '기타'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    qr_code = models.ImageField(upload_to='qr_codes/')

    # 현재 수강중인 강의 추가
    current_course_name = models.CharField(max_length=20, default="수강중인 강의 없음", null=True)

    def __str__(self):
        return self.name