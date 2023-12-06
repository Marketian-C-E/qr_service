from django import forms
from course.models import Course, ClassAttend
from django.utils.safestring import mark_safe
from django.forms import DateInput, TimeInput


# 강의 추가 폼
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        labels = {
            'course_name': mark_safe('<b>강의 제목</b>'),
            'teacher_name': '강사명',
            'division_name': '분반 이름',
            'start_date': '시작 날짜',
            'start_at': '시작 시간',
            'end_at': '종료 시간',
            'hours': '진행 시간(시간) - 숫자만 기입 ex) 3',
        }
        
        widgets = {
            'start_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_at': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_at': TimeInput(attrs={'class': 'form-control', 'type': 'time'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['division_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['teacher_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_at'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_at'].widget.attrs.update({'class': 'form-control'})
        self.fields['hours'].widget.attrs.update({'class': 'form-control'})

class ClassAttendInForm(forms.ModelForm):
    class Meta:
        model = ClassAttend
        fields = '__all__'
        exclude = ['end_at', 'submit_survey', 'attend_state']