from django.db import models
from user.models import Student, Division

from datetime import time
# Create your models here.


# 강의
class Course(models.Model):
    course_name = models.CharField(max_length=50)
    teacher_name = models.CharField(max_length=20)
    division_name = models.ForeignKey(Division, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_at = models.TimeField()
    end_at = models.TimeField()
    hours = models.IntegerField()
    
    def __str__(self):
        return f'[{self.division_name}] {self.course_name} (강사: {self.teacher_name}) - 수업시간: {self.hours}'



# 강의에 대한 학생 출석
class ClassAttend(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_at = models.TimeField(default=time(0, 0))
    end_at = models.TimeField(default=time(0, 0))

    attend_state = models.IntegerField(default=0)   # --> 2(출석) 1(지각) 0(결석)
    # l(지각) 부분은 수업 정상 입실시간의 15분 뒤에 입실 시간이 찍히면(비교), 지각으로 처리

    def __str__(self):
        return f'[{self.course_id.course_name} 출석] {self.student_id.name}'
