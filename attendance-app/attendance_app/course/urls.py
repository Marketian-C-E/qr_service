from django.urls import path, include
from course import views

from django.contrib.auth import views as auth_views

app_name = 'course'

urlpatterns = [
    path('<int:pk>', views.course_list, name='course_list'),
    path('detail/<int:pk>/', views.course_detail, name='course_detail'),
    

    
    path('create/', views.create_course, name='create_course'),
    path('edit/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('download/<int:pk>', views.download_attendance, name='download_attendance' ),


    path('attendance_division_list/', views.attendance_divison_list, name='attendance_division_list'),
    path('attendance_course_list/<int:pk>/', views.attendance_course_list, name='attendance_course_list'),
    path('attendance_course_board/<int:pk>/', views.attendance_course_board, name='attendance_course_board'),


    path('QRScanner_in/<int:pk>/', views.QRScanner_in, name='QRScanner_in'),
    path('QRScanner_out/<int:pk>/', views.QRScanner_out, name='QRScanner_out'),
    path('attendance_check_in', views.attendance_check_in, name='attendance_check_in'),
    path('attendance_check_in_success/<int:pk>/', views.attendance_check_in_success, name='attendance_check_in_success'),
    path('attendance_check_out', views.attendance_check_out, name='attendance_check_out'),
    
    path('student_attendance_update', views.student_attendance_update, name='student_attendance_update'),

]
