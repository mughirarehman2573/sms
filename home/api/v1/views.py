import math
import base64
import face_recognition
from io import BytesIO

import requests
from PIL import Image
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from home.permissions import AdminBasedPermission, TeacherBasedPermission, StudentBasedPermission
from home.api.v1.serializers import (SignupSerializer, StudentSerializer,
                                     StudentProfileSerializer, UniversitySerializer,
                                     CampusSerializer, DepartmentSerializer,
                                     ProgramSerializer, CourseSerializer, EnrollmentSerializer,
                                     AttendanceSerializer, AttendanceLogSerializer, DisciplineSerializer,
                                     LeaveTypeSerializer, LeaveSerializer, UserSerializer)
from home.models import Student, StudentProfile, University, Campus, Department, Program, Course, Enrollment, \
    Attendance, AttendanceLog, Discipline, LeaveType, Leave
from users.models import User


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]
    permission_classes = [AllowAny]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [StudentBasedPermission]


class StudentProfileViewSet(ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AdminBasedPermission]
    http_method_names = ["get", "put", "patch", "retrieve"]


class UniversityViewSet(ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [AdminBasedPermission]


class CampusViewSet(ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [AdminBasedPermission]


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AdminBasedPermission]


class ProgramViewSet(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [AdminBasedPermission]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AdminBasedPermission]


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [AdminBasedPermission]


def haversine_(l1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(l1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - l1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [TeacherBasedPermission]

    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        campus_id = request.data.get('campus_id')
        student_latitude = request.data.get('latitude')
        student_longitude = request.data.get('longitude')

        if not (student_latitude and student_longitude):
            return Response({'message': 'Latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student_latitude = float(student_latitude)
            student_longitude = float(student_longitude)
        except ValueError:
            return Response({'message': 'Invalid latitude or longitude.'}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, id=student_id)
        campus = get_object_or_404(Campus, id=campus_id)

        distance = haversine_(student_latitude, student_longitude, float(campus.latitude), float(campus.longitude))

        if distance <= 500:
            attendance = Attendance.objects.create(student=student, latitude=student_latitude,
                                                   longitude=student_longitude, duration=0)
            AttendanceLog.objects.create(status='Punch In', attendance=attendance)
            return Response({'message': 'Attendance marked successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not within the 100 meters radius of the campus.'},
                            status=status.HTTP_400_BAD_REQUEST)


class AttendanceLogViewSet(ModelViewSet):
    queryset = AttendanceLog.objects.all()
    serializer_class = AttendanceLogSerializer
    permission_classes = [AdminBasedPermission]


class DisciplineViewSet(ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [AdminBasedPermission]


class LeaveTypeViewSet(ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [StudentBasedPermission]


class LeaveViewSet(ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer


class LeaveApprovalViewSet(ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [TeacherBasedPermission]
    http_method_names = ['get', 'patch', 'retrieve']


def index(request):
    return render(request, 'index.html')


def get_current_location():
    try:
        response = requests.get('http://ipinfo.io/json')
        data = response.json()
        location = data['loc'].split(',')
        latitude = float(location[0])
        longitude = float(location[1])
        return latitude, longitude
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def capture_image(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)
        face_encodings = face_recognition.face_encodings(image_np)

        if face_encodings:
            face_encoding = face_encodings[0]

            for user in User.objects.all():
                user_image = face_recognition.load_image_file(user.face_encoding.path)
                user_face_encodings = face_recognition.face_encodings(user_image)

                if user_face_encodings:
                    user_face_encoding = user_face_encodings[0]
                    match = face_recognition.compare_faces([user_face_encoding], face_encoding)
                    if match[0]:
                        student = get_object_or_404(Student, user=user)
                        campus = get_object_or_404(Campus, id=1)
                        lat, lon = get_current_location()

                        distance = haversine_(lat, lon, float(campus.latitude),
                                              float(campus.longitude))

                        if distance <= 100:
                            attendance = Attendance.objects.create(student=student, latitude=lat,
                                                                   longitude=lon, duration=0)
                            AttendanceLog.objects.create(status='Punch In', attendance_id=attendance.id)
                            return JsonResponse({'name': user.name, 'status': 'Attendance marked'})
                        return JsonResponse({"status": "you are out of range"})

            return JsonResponse({'status': 'No match found'})

    return JsonResponse({'status': 'Invalid request'})



class StudentsUnderTeacherViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [TeacherBasedPermission]

    def get_queryset(self):
        return super().get_queryset().filter(user__user_type="teacher")


class StudentListViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

