from django.urls import path
from . import views

urlpatterns = [
    # All Roles
    path('courses', views.course_list, name='course-list'),
    
    # Admin
    path('admin/course/<int:pk>', views.course_detail, name='course-detail'),
    
    # Student
    path('student/schedule', views.student_courses, name='student-courses'),
    path('student/add-course/<int:course_id>', views.add_course_to_schedule, name='add_course_to_schedule'),
    path('student/remove-course/<int:course_id>', views.remove_course_from_schedule, name='remove_course_from_schedule')
]
