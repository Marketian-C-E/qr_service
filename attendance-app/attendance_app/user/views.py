from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from user.models import Student, Division
from course.models import ClassAttend, Course
from django.db.models import Q

from django.contrib.auth import login, authenticate

from user.forms import SignUpForm, ClientForm
from django.contrib import messages

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password
from django.core.files import File
from pathlib import Path

from io import BytesIO

from user.forms import DivisionForm
from django.contrib.auth import update_session_auth_hash

from user.forms import DivisionForm, StudentEditForm, PasswordChangeFormCustom

from django.contrib.auth.decorators import login_required, user_passes_test

import qrcode, os
# Create your views here.
# 관리자 페이지
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def admin_home(request):
    return render(request, 'user/admin/admin_home.html')


# 학생 계정 추가 
def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        client_form = ClientForm(request.POST)
        
        if signup_form.is_valid() and client_form.is_valid():
            # 회원가입 후 자동 로그인
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password')
            password2 = signup_form.cleaned_data.get('password2')

            # 비밀번호가 유효하지않음.
            if password != password2:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
                return render(request, 'user/student/signup.html', {'signup_form': signup_form, 'client_form': client_form})
            
            else:
                try:
                    # 비밀번호 검증
                    validate_password(password)
                    validate_password(password2)
                    
                    # 비밀번호 암호화
                    hashed_password = make_password(password)
                    
                    user = signup_form.save(commit=False)
                    user.password = hashed_password  # 암호화된 비밀번호 설정
                    user.save()
                    
                    student = client_form.save(commit=False)
                    student.user = user

                     # qr코드 생성
                    qr_date = student.name
                    qr = qrcode.QRCode()
                    qr.add_data(qr_date)
                    qr.make()
                    img = qr.make_image(fill_color="black", back_color="white")
                    
                    # 이미지 파일을 BytesIO 객체에 저장
                    image_buffer = BytesIO()
                    img.save(image_buffer, format='PNG')
                    image_buffer.seek(0)

                    # File 객체 생성
                    file_name = f"{student.name}_qr.png"  # 이미지 파일명 설정
                    file = File(image_buffer, name=file_name)

                    student.qr_code = file
                    student.save()
                    user = authenticate(username=username, password=password)
                    student.save()
                    
                    # 자동 로그인
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return render(request, 'home/home.html')
                    
                except ValidationError as validation_error:
                    messages.error(request, f"{validation_error}")
                    return render(request, 'user/student/signup.html', {'signup_form': signup_form, 'client_form': client_form})
                
    else:
        signup_form = SignUpForm()
        client_form = ClientForm()

    context = {
        'signup_form': signup_form, 
        'client_form': client_form,
        
        }
    
    return render(request, 'user/student/signup.html', context)


#  학생 정보
@login_required
def student_detail(request):
    user = User.objects.get(pk=request.user.pk)
    student = Student.objects.get(user_id=request.user.pk)
    division = Division.objects.get(pk=student.division_id)
    
    context = {
        'user': user,
        'student': student,
        'division': division,
    }

    return render(request, 'user/student/student_detail.html', context)
    
    
    
#  학생 정보 수정
@login_required
def edit_student(request):
    student = request.user.student

    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('user:student_detail')  # Replace 'profile' with the appropriate URL name for the profile page
    else:
        form = StudentEditForm(instance=student)

    return render(request, 'user/student/edit_student.html', {'form': form})


# 비밀번호 수정
@login_required
def edit_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeFormCustom(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)

            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('user:student_detail')  # Replace 'profile' with the appropriate URL name for the profile page
    else:
        password_form = PasswordChangeFormCustom(request.user)

    return render(request, 'user/student/edit_password.html', {'password_form': password_form})





## QR 코드 보여주기
# 입실    
@login_required
def show_in_qr(request):
    return render(request, 'user/student/show_in_qr.html')


# 퇴실    
@login_required
def show_out_qr(request):
    return render(request, 'user/student/show_out_qr.html')


########## 관리자 권한 필요 ################
## 분반
# 분반 목록
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def division_list(request):
    divison = Division.objects.all()
    
    context = {'division': divison}
    return render(request, 'user/admin/admin_division_list.html', context)


# 분반 추가
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def create_division(request):
    if request.method == 'POST':
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:division_list')  # 적절한 URL로 리다이렉트

    else:
        form = DivisionForm()

    return render(request, 'user/admin/admin_create_division.html', {'form': form})



# 분반 수정
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def edit_division(request, division_id):
    division = get_object_or_404(Division, pk=division_id)

    if request.method == 'POST':
        form = DivisionForm(request.POST, instance=division)
        if form.is_valid():
            form.save()
            return redirect('user:division_list')  # 적절한 URL로 리다이렉트

    else:
        form = DivisionForm(instance=division)

    return render(request, 'user/admin/admin_edit_division.html', {'form': form, 'division': division})



# 분반 삭제
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def delete_division(request, division_id):
    division = get_object_or_404(Division, pk=division_id)
    
    if request.method == 'POST':
        try:
            division.delete()
            return redirect('user:division_list')  # 적절한 URL로 리다이렉트
        
        except ProtectedError:
            '''학생이 존재하는 분반을 지울시 생기는 오류'''
            
            # 해당 분반에 가입되어있는 학생 정보 전달
            users = User.objects.filter(student__division_id=division_id)
            
            context = {
                'users': users,
                
            }
            
            return render(request, 'user/error_page/division_protected_error.html', context)
    
    return render(request, 'user/admin/admin_delete_division.html', {'division': division})


# 학생 출석 정보
@login_required
def student_attendance_detail(request):
    student = request.user.student
    division = Division.objects.get(pk=student.division_id)
    course = Course.objects.filter(division_name_id=student.division_id)
    class_attend = ClassAttend.objects.filter(student_id_id=student.pk)
    


    context ={
        'student': student,
        'division': division,
        'course': course,
        'class_attend': class_attend,

    }

    return render(request, 'user/student/student_attendance_detail.html', context)



@login_required
def delete_student(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # 비밀번호가 맞는 경우 회원 삭제
            user.delete()
            return redirect('home')  # 회원탈퇴 후 리다이렉션할 URL
        else:
            # 비밀번호가 틀린 경우 에러 메시지 출력
            error_message = '비밀번호가 올바르지 않습니다.'
            return render(request, 'user/student/delete_student.html', {'error_message': error_message})
    else:
        return render(request, 'user/student/delete_student.html')
