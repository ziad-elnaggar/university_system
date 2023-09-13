from django.urls import path
from .views import register_user, login_user

urlpatterns = [
    path('register', register_user, name='register-user'),
    path('login/admin', login_user, {'role': 'Admin'}, name='admin-login'),
    path('login/student', login_user, {'role': 'Student'}, name='student-login'),
]

