from cProfile import Profile

from django.http import HttpRequest
from allauth.account import app_settings as allauth_settings
from allauth.utils import generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from users.models import User
from home.models import (StudentProfile, Student, University,
                         Campus, Department, Program, Course,
                         Enrollment, Attendance, AttendanceLog, Discipline, LeaveType, Leave)

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'user_type')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            },
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request


    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


def email_address_exists(email):
    return User.objects.filter(email=email).exists()


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'full_name', 'address', 'mobile', 'country', 'guardian_contact', 'student_photo']

class StudentSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(required=False)
    class Meta:
        model = Student
        fields = ['id', 'program', 'user', 'enrollment_number', 'date_of_joining', 'date_of_birth',
                  'status', 'type', 'profile']

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile', None)
    #     student = Student.objects.create(**validated_data)
    #     if profile_data:
    #         StudentProfile.objects.create(student=student, **profile_data)
    #     else:
    #         StudentProfile.objects.create(student=student)
    #     return student

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()




class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        exclude = ['is_deleted', 'created_at', 'updated_at']


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        exclude = ['is_deleted', 'created_at', 'updated_at']



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ['is_deleted', 'created_at', 'updated_at']

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        exclude = ['is_deleted', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ['is_deleted', 'created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        exclude = ['is_deleted', 'created_at', 'updated_at']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ['is_deleted', 'created_at', 'updated_at']


class AttendanceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLog
        exclude = ['is_deleted', 'created_at', 'updated_at']


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        exclude = ['is_deleted', 'created_at', 'updated_at']


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        exclude = ['is_deleted', 'created_at', 'updated_at']


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        exclude = ['is_deleted', 'created_at', 'updated_at']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'user_type', 'face_encoding']