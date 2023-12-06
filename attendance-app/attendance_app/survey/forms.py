from django import forms
from survey.models import Survey, SurveyReply

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = (
            'question1', 
            'question2', 
            'question3',
            'question4',
            'question5',
            'question6',
            'question7',
            'question8',
            'question9',
            'question10',
            'question11',
            'question12',
            'question13',
            'question14',
            'question15',
            
            )
        
        
        widgets = {
            'course_id': forms.Select(attrs={'class': 'form-select'}),
            'question1': forms.TextInput(attrs={'class': 'form-control'}),
            'question2': forms.TextInput(attrs={'class': 'form-control'}),
            'question3': forms.TextInput(attrs={'class': 'form-control'}),
            'question4': forms.TextInput(attrs={'class': 'form-control'}),
            'question5': forms.TextInput(attrs={'class': 'form-control'}),
            'question6': forms.TextInput(attrs={'class': 'form-control'}),
            'question7': forms.TextInput(attrs={'class': 'form-control'}),
            'question8': forms.TextInput(attrs={'class': 'form-control'}),
            'question9': forms.TextInput(attrs={'class': 'form-control'}),
            'question10': forms.TextInput(attrs={'class': 'form-control'}),
            'question11': forms.TextInput(attrs={'class': 'form-control'}),
            'question12': forms.TextInput(attrs={'class': 'form-control'}),
            'question13': forms.TextInput(attrs={'class': 'form-control'}),
            'question14': forms.TextInput(attrs={'class': 'form-control'}),
            'question15': forms.TextInput(attrs={'class': 'form-control'}),

        }
        
        
        labels = {
            'question1': '질문 1',
            'question2': '질문 2',
            'question3': '질문 3',
            'question4': '질문 4',
            'question5': '질문 5',
            'question6': '질문 6',
            'question7': '질문 7',
            'question8': '질문 8',
            'question9': '질문 9',
            'question10': '질문 10',
            'question11': '질문 11',
            'question12': '질문 12',
            'question13': '질문 13',
            'question14': '질문 14',
            'question15': '질문 15',
        }
        
        
# 학생 설문 응답
class SurveyReplyForm(forms.ModelForm):
    class Meta:
        model = SurveyReply
        fields = (
            'reply1', 
            'reply2', 
            'reply3',
            'reply4',
            'reply5',
            'reply6',
            'reply7',
            'reply8',
            'reply9',
            'reply10',
            'reply11',
            'reply12',
            'reply13',
            'reply14',
            'reply15',
                  
            )

