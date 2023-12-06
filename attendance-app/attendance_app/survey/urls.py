from django.urls import path, include
from survey import views


app_name = 'survey'

urlpatterns = [
    path('', views.survey_division_list, name='survey_division_list'),
    path('course_survey/<int:pk>', views.survey_list, name='survey_list'),
    path('detail/<int:pk>/', views.survey_detail, name='survey_detail'),
    path('reply_detail/<int:pk>/', views.survey_reply_detail, name='survey_reply_detail'),
    
    # 설문 목록 다운로드
    path('download/<int:pk>/', views.download_surveyreply, name='download_surveyreply'),
    
    
    # 학생 설문 페이지 
    path('survey_student_reply/<int:pk>/', views.survey_student_reply, name='survey_student_reply'),
    path('survey_student_submit/', views.survey_student_submit, name='survey_student_submit'),
    
    # path('create/', views.create_course, name='create_course'),
    # path('edit/<int:pk>/', views.edit_course, name='edit_course'),
    # path('delete/<int:pk>/', views.delete_course, name='delete_course'),
]
