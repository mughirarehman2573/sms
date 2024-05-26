from datetime import timezone

from django.db import models
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from home.model_mixins import BaseModel
from users.models import User
from datetime import date


class University(BaseModel):
    university_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Campus(BaseModel):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department(BaseModel):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Program(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    duration_years = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Student(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=20, unique=True)
    date_of_joining = models.DateField(null=True)
    date_of_birth = models.DateField(null=True)
    STATUS_CHOICES = {
        'Regular': 'Regular',
        'Irregular': 'Irregular',
    }
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Regular', null=True)
    TYPE_CHOICES = {
        'Regular': 'Regular',
        'Transfer': 'Transfer',
    }
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Regular', null=True)

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
    #     StudentProfile.objects.create(student_id=self.id)
    #     super(Student, self).save(*args, **kwargs)


class StudentProfile(BaseModel):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    guardian_contact = models.IntegerField(null=True, blank=True)
    student_photo = models.ImageField(upload_to='student_photos/ ', null=True, blank=True)

    def __str__(self):
        return self.full_name


class Course(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credit_hours = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Enrollment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField()
    year = models.IntegerField()
    grade = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name}"


class Attendance(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.created_at}"


class AttendanceLog(BaseModel):
    STATUS_CHOICES = {
        'Punch In': 'Punch In',
        'Punch Out': 'Punch Out',
    }

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.attendance.student.user.username} - {self.status}"


class Discipline(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    incident_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.student.user.username} - {self.incident_date}"


class LeaveType(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Leave(BaseModel):
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=250)
    APPROVAL_CHOICES = {
        'Pending': 'Pending',
        'Approved': 'Approved',
        'Rejected': 'Rejected'
    }

    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES)

    def __str__(self):
        return self.leave_type.title


class AttendanceStatsView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        today = date.today()

        present_logs = AttendanceLog.objects.filter(
            Q(status='Punch In') & Q(attendance__created_at__date=today)
        ).distinct('attendance__student')
        present_count = present_logs.count()

        on_leave = Leave.objects.filter(
            Q(start_date__lte=today) & Q(end_date__gte=today) & Q(approval_status='Approved')
        ).distinct('student')
        on_leave_count = on_leave.count()


        total_students = Student.objects.count()
        absent_count = total_students - present_count - on_leave_count

        data = {
            "present": present_count,
            "absent": absent_count,
            "on_leave": on_leave_count,
        }
        return Response(data)


class StudentAttendanceStatsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"message": "student not found"})

        today = date.today()

        present_logs = AttendanceLog.objects.filter(
            Q(status='Punch In') & Q(attendance__student=student)
        ).distinct('attendance__created_at')
        present_count = present_logs.count()

        on_leave = Leave.objects.filter(
            Q(start_date__lte=today) & Q(end_date__gte=today) & Q(student=student) & Q(approval_status='Approved')
        )
        on_leave_count = on_leave.count()


        total_days = (
                    today - student.created_at.date()).days + 1
        absent_count = total_days - present_count - on_leave_count

        data = {
            "present": present_count,
            "absent": absent_count,
            "on_leave": on_leave_count,
        }

        return Response(data)