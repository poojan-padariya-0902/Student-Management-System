from django.urls import path
from .views import *

urlpatterns = [
    
    # Home Urls
    path('', home, name='home'),
    
    # Student Management Urls
    path('students/', student_list, name='student_list'),
    path('students/<int:pk>/', student_detail, name='student_detail'),
    path('students/add/', student_create, name='student_create'),
    path('students/<int:pk>/edit', student_edit, name='student_edit'),
    path('students/<int:pk>/delete', student_delete, name='student_delete'),
    
    # Courses Management Urls
    path('courses/', course_list, name='course_list'),
    path('courses/<int:pk>/', course_detail, name='course_detail'),
    path('courses/add/', course_create, name='course_create'),
    path('courses/<int:pk>/edit', course_edit, name='course_edit'),
    path('courses/<int:pk>/delete', course_delete, name='course_delete'),
    
    # Enrollments Management Urls
    path('enrollments/', enrollment_list, name='enrollment_list'),
    path('enrollments/add', enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/grade', enrollment_update_grade, name='enrollment_update_grade'),
    path('enrollments/<int:pk>/delete', enrollment_delete, name='enrollment_delete'),
    
    # Reports Management Urls
    path('reports/', report_overview, name='reports_overview'),
    path('reports/student/<int:pk>', student_transcript, name='student_transcript'),
    
]
