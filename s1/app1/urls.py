from django.urls import path
from .views import auth_page, register_user, login_user, teacher_dashboard,student_dashboard,admin_dashboard, teacher_sections,section_students, logout_user
from .views import create_section, student_detail,mark_attendance, student_attendance
from .views import create_assignment, student_assignments, submit_assignment
from .views import view_teachers, view_students, assign_student_section, assign_teacher_section, edit_section, delete_section
urlpatterns = [
    #common urls
    path('', auth_page, name='auth_page'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    #admin urls
    path('dashboard/admin/teachers/', view_teachers, name='view_teachers'),
    path('dashboard/admin/students/', view_students, name='view_students'),
    path('dashboard/admin/assign-teacher/', assign_teacher_section, name='assign_teacher_section'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/create-section/', create_section, name='create_section'),
    path('dashboard/admin/edit-section/<int:section_id>/', edit_section, name='edit_section'),
    path('dashboard/admin/delete-section/<int:section_id>/', delete_section, name='delete_section'),
    path('dashboard/admin/assign-student/', assign_student_section, name='assign_student_section'),
    #teacher urls
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('sections/', teacher_sections, name='teacher_sections'),
    path('attendance/<int:section_id>/', mark_attendance, name='mark_attendance'),
    path('assignment/create/<int:section_id>/', create_assignment, name='create_assignment'),

    #student urls
    
    path('student/', student_dashboard, name='student_dashboard'),
    path('sections/<int:section_id>/', section_students, name='section_students'),
    path('student/<uuid:student_id>/', student_detail, name='student_detail'),
    path('my-attendance/', student_attendance, name='student_attendance'),
    path('my-assignments/', student_assignments, name='student_assignments'),
    path('submit/<int:assignment_id>/', submit_assignment, name='submit_assignment'),
]