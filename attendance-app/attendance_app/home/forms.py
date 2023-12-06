from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': '잘못된 사용자명 또는 비밀번호입니다.',
        'inactive': '비활성화된 계정입니다.',
    }
