from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AdminBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied('Only Admin can have permissions to access this page')
        elif request.user.user_type == 'admin':
            return True
        elif request.user.is_superuser:
            return True
        else:
            raise PermissionDenied('Only Admin can have permissions to access this page')


class StudentBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied('Only Students have permission to access this page')
        elif request.user.user_type == 'student':
            return True
        else:
            raise PermissionDenied('Only Students have permission to access this page')


class TeacherBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise PermissionDenied('Only Teachers have permission to access this page')
        elif request.user.user_type == 'teacher':
            return True
        else:
            raise PermissionDenied('Only Teachers have permission to access this page')
