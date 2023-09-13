from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'

class IsStudentUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Student'