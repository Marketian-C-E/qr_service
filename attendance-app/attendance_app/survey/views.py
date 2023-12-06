# survey/views.py
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from course.models import Course, ClassAttend
from survey.models import Survey, SurveyReply
from user.models import Division, Student
from survey.forms import SurveyReplyForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.http import HttpResponse

# 엑셀 다운로드
import openpyxl
from openpyxl.utils import get_column_letter
import pandas as pd
import urllib.parse

# Create your views here.
# 설분 문반 선택 리스트
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def survey_division_list(request):
    division = Division.objects.all()
    
    context = {
        'division': division,     
        
    }
    
    return render(request, 'survey/survey_division_list.html', context)



# 설문 리스트
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def survey_list(request, pk):
    division = Division.objects.get(pk=pk)
    course = Course.objects.filter(division_name_id=pk)
    
    
    context = {
        'division': division,
        'course': course,
        
        }
    return render(request, 'survey/survey_list.html', context)

    

# 설문 상세
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def survey_detail(request, pk):
    # 쿼리 변수 초기화
    survey = None
    course = None
    divison = None
    survey_reply = None
    
    # 쿼리 조회 시도
    try:
        survey = Survey.objects.get(course_id=pk)
        course = Course.objects.get(pk=survey.course_id.pk)
        division = Division.objects.get(pk=course.division_name_id)
    
    # 쿼리 조회 결과가 없을 경우 패스
    except Survey.DoesNotExist:
        pass
    
    except Course.DoesNotExist:
        pass
    
    
    # survey = get_object_or_404(Survey, course_id=pk)
    # course = get_object_or_404(Course, pk=survey.course_id.pk)
    
    if survey is not None:
        survey_reply = SurveyReply.objects.filter(survey_id = survey.pk)
    
    
    context = {
        'survey': survey,
        'course': course,
        'division': division,
        'survey_reply': survey_reply,
        
        }
    
    return render(request, 'survey/survey_detail.html', context)


# 설문 상세
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def survey_reply_detail(request, pk):
    survey_reply = get_object_or_404(SurveyReply, pk=pk)
    survey = get_object_or_404(Survey, pk=survey_reply.survey_id.pk)
    course = get_object_or_404(Course, pk=survey.course_id.pk)
    
    context = {
        'survey_reply': survey_reply,
        'survey': survey,
        'course': course,
        }
    
    return render(request, 'survey/survey_reply_detail.html', context)


# 학생 설문 페이지
@login_required
def survey_student_reply(request, pk) :
    # 해당 수강생이 현재 과목을 듣고 있는지 확인
    # 해당 학생과 surveyReply를 이어주기 위해
    student = Student.objects.get(pk=pk)
    student_course = Course.objects.get(course_name=student.current_course_name)
    
    # 해당 과목 survey
    course_survey = Survey.objects.get(course_id = student_course)
    
    context = { 
        'student_course' : student_course,
        'course_survey' : course_survey,
        'student' : student,
        
    }

    print(f'{course_survey.question1 = }')
    print(f'{course_survey.question2 = }')
    print(f'{course_survey.question3 = }')
    return render(request, 'survey/survey_student_reply.html', context)



# (사용 안함)학생 설문 제출 처리
"""
@login_required
def survey_student_submit(request):
    ''' 사용 안함 '''
    if request.method == 'POST':
        form = SurveyReplyForm(request.POST)
        if form.is_valid():
            student_id = request.POST.get('student_id')
            survey_id = request.POST.get('survey_id')
            survey_reply = form.save(commit=False)

            survey_reply.student_id = Student.objects.get(id = student_id)  # 학생 ID 설정
            survey_reply.survey_id = Survey.objects.get(id = survey_id)
            survey_reply.submit_survey = True
            survey_reply.save()

            # 이 코드는 퇴실 QR까지 찍으면 
            # survey_reply.student_id.current_course_name = "수강중인 강의 없음"

            survey_reply.student_id.save()
            # 추가적인 처리 수행
            return redirect('user:show_out_qr')
        else:
            errors = form.errors.as_text()
            # 폼이 유효하지 않은 경우, 오류 처리
    else:
        form = SurveyReplyForm()
        
"""


@login_required
def survey_student_submit(request):
    ''' 설문 조사 후 바로 퇴실 처리 '''
    if request.method == 'POST':
        form = SurveyReplyForm(request.POST)
        if form.is_valid():

            student_id = request.POST.get('student_id')
            survey_id = request.POST.get('survey_id')
            survey_reply = form.save(commit=False)


            ### 설문 내용 저장
            survey_reply.student_id = Student.objects.get(id = student_id)  # 학생 ID 설정
            survey_reply.survey_id = Survey.objects.get(id = survey_id)
            survey_reply.submit_survey = True
            survey_reply.save()

            # 이 코드는 퇴실 QR까지 찍으면 
            # survey_reply.student_id.current_course_name = "수강중인 강의 없음"

            survey_reply.student_id.save()
            # 추가적인 처리 수행
            


            ### 출석 저장
            
            # 현재 강의에 대한 기존 출결 기록 가져오기
            # 예외처리
            try:
                '''ClassAttend Update 구문 실행'''
                survey = Survey.objects.get(pk=survey_id)
                course = Course.objects.get(pk=survey.course_id.pk)
                
                # ClassAttend 객체 가져오기
                student_class_attend = ClassAttend.objects.get(Q(course_id=course) & Q(student_id=student_id))
                
                ## 출석 및 설문 제출시간 업데이트
                # 설문 제출 시간
                current_time = datetime.now().time()
                student_class_attend.end_at = current_time
                
                # 출석 상태 -> 인정(2)
                student_class_attend.attend_state = 2
            
                # 객체 저장
                student_class_attend.save()
                
                
                # 학생 든는 수업 없음으로 바꾸기
                student = Student.objects.get(pk=student_id)
                student.current_course_name = '수강중인 강의 없음'
                student.save()
                
                
            except ObjectDoesNotExist:
                '''객체를 못가져올 시 생기는 예외 처리'''
                pass
            
            
            except MultipleObjectsReturned:
                '''이미 설문제출을 했는데 또 제출하려는 경우'''
                pass



            # 제출 완료시 메인페이지로
            return redirect('home:home')
        else:
            errors = form.errors.as_text()
            # 폼이 유효하지 않은 경우, 오류 처리
    else:
        form = SurveyReplyForm()


# 강의 출석현황 xlsx 다운로드
@user_passes_test(lambda u: u.is_staff, login_url='/') # 권한 없으면 홈으로
def download_surveyreply(request, pk):
    """강의 평가 xlsx 다운로드"""
    # pk -> 강의(course) pk 값
    course_name = Course.objects.get(pk=pk).course_name
    # print(course_name)
    survey = Survey.objects.get(pk=pk)  # survey 질문 pk값
    surveyreplies = SurveyReply.objects.filter(survey_id_id=survey.pk).order_by('pk')  #  survey 답변 객체 모음
    
    # 특정 강의에 대한 질문 객체들 모음
    # print(len(surveyreplies))
    # print(list(surveyreplies.values_list('reply1', flat=True)))
    
    # 질문 10개 순회
    # print(list(surveyreplies.values_list('reply10', flat=True)))
        
    data = {
        f'[질문1] {survey.question1}': list(surveyreplies.values_list('reply1', flat=True)),  # 질문1에 대한 답변
        
        f'[질문2] {survey.question2}': list(surveyreplies.values_list('reply2', flat=True)),  # 질문2에 대한 답변
        
        f'[질문3] {survey.question3}': list(surveyreplies.values_list('reply3', flat=True)),  # 질문3에 대한 답변
        
        f'[질문4] {survey.question4}': list(surveyreplies.values_list('reply4', flat=True)),  # 질문4에 대한 답변
        
        f'[질문5] {survey.question5}': list(surveyreplies.values_list('reply5', flat=True)),  # 질문5에 대한 답변
        
        f'[질문6] {survey.question6}': list(surveyreplies.values_list('reply6', flat=True)),  # 질문6에 대한 답변
        
        f'[질문7] {survey.question7}': list(surveyreplies.values_list('reply7', flat=True)),  # 질문7에 대한 답변
        
        f'[질문8] {survey.question8}': list(surveyreplies.values_list('reply8', flat=True)),  # 질문8에 대한 답변
        
        f'[질문9] {survey.question9}': list(surveyreplies.values_list('reply9', flat=True)),  # 질문9에 대한 답변
        
        f'[질문10] {survey.question10}': list(surveyreplies.values_list('reply10', flat=True)),  # 질문10에 대한 답변

        f'[질문11] {survey.question11}': list(surveyreplies.values_list('reply11', flat=True)),  # 질문11에 대한 답변

        f'[질문12] {survey.question12}': list(surveyreplies.values_list('reply12', flat=True)),  # 질문12에 대한 답변

        f'[질문13] {survey.question13}': list(surveyreplies.values_list('reply13', flat=True)),  # 질문13에 대한 답변

        f'[질문14] {survey.question14}': list(surveyreplies.values_list('reply14', flat=True)),  # 질문14에 대한 답변

        f'[질문15] {survey.question15}': list(surveyreplies.values_list('reply15', flat=True)),  # 질문15에 대한 답변
        
    }
    
    # pandas로 CSV 데이터 생성 (예시)
    # data = {'이름': ['Alice', 'Bob', 'Charlie'],
    #         '나이': [25, 30, 35]}
    
    df = pd.DataFrame(data)

    # CSV 파일로 데이터를 저장
    response = HttpResponse(content_type='text/csv', charset='utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="{urllib.parse.quote(course_name)}.csv"'
    df.to_csv(path_or_buf=response, index=False, encoding='utf-8-sig')

    return response