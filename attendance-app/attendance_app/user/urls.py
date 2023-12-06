# user.urls

from django.urls import path

from user import views

urlpatterns = [
    path('admin_home', views.admin_home, name='admin_home'),

    path('student_detail/', views.student_detail, name='student_detail'),
    path('student_attendance_detail/', views.student_attendance_detail, name='student_attendance_detail'),
    path('edit_student/', views.edit_student, name='edit_student'),
    path('edit_passowrd/', views.edit_password, name='edit_password'),
    path('delete_student/', views.delete_student, name='delete_student'),

    path('signup/', views.signup, name='signup'),
    
    path('show_in_qr/', views.show_in_qr, name='show_in_qr'),
    path('show_out_qr/', views.show_out_qr, name='show_out_qr'),
    
    path('division_list/', views.division_list, name='division_list'),
    path('create_division/', views.create_division, name='create_division'),
    path('edit_division/<int:division_id>/', views.edit_division, name='edit_division'),
    path('delete_division/<int:division_id>/', views.delete_division, name='delete_division'),

]
