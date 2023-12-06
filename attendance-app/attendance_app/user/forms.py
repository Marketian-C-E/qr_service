from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User

from user.models import Student
from user.models import Division

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

# Forms
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='비밀번호', help_text='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='비밀번호 확인', help_text='')

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        labels = {
            'username': 'ID',
            'password': '비밀번호',
            'password2': '비밀번호 확인',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  # 도움말 텍스트 비움
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', '비밀번호와 비밀번호 확인이 일치하지 않습니다.')

        return cleaned_data
    



class ClientForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
        ('O', '기타'),
    )

    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='생년월일')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label='성별')
    division = forms.ModelChoiceField(queryset=Division.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='분반')

    class Meta:
        model = Student
        fields = ['name', 'birth_date', 'gender', 'division']
        labels = {
            'name': '이름',
            'birth_date': '생년월일',
            'gender': '성별',
            'division': '학과',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


# 분반 폼
class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name']
        labels = {
            'name': '분반 이름',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    

# 학생 정보 수정 폼
class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'birth_date', 'gender', 'division']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
        }



class PasswordChangeFormCustom(PasswordChangeForm):
    old_password = forms.CharField(label='기존 비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='새로운 비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='새로운 비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        validate_password(password)
        return password

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = _('비밀번호는 8자 이상이어야 하며, 최소 하나의 숫자, 하나의 대문자, 하나의 소문자, 하나의 특수 문자를 포함해야 합니다.')

    error_messages = {
        'password_incorrect': _('현재 비밀번호가 올바르지 않습니다.'),
        'password_mismatch': _('새로운 비밀번호가 일치하지 않습니다.'),
        'password_too_short': _('비밀번호가 너무 짧습니다. 최소 8자 이상이어야 합니다.'),
        'password_common': _('너무 흔한 비밀번호입니다. 다른 비밀번호를 사용해주세요.'),
        'password_numeric': _('비밀번호는 숫자로만 이루어질 수 없습니다.'),
    }