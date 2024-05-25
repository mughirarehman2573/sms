from django.contrib import admin
from .models import (
    University, Campus, Department, Program, Student, StudentProfile,
    Course, Enrollment, Attendance, AttendanceLog, Discipline, LeaveType, Leave
)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'university_code', 'country', 'phone_number', 'email')
    search_fields = ('name', 'university_code', 'country')
    list_filter = ('country',)
    ordering = ('name',)


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'city', 'latitude', 'longitude')
    search_fields = ('name', 'university__name', 'city')
    list_filter = ('city', 'university')
    ordering = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus', 'code')
    search_fields = ('name', 'code', 'campus__name')
    list_filter = ('campus',)
    ordering = ('name',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'code', 'duration_years')
    search_fields = ('name', 'code', 'department__name')
    list_filter = ('department',)
    ordering = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'program', 'enrollment_number', 'date_of_joining', 'status', 'type')
    search_fields = ('user__username', 'enrollment_number', 'program__name')
    list_filter = ('status', 'type', 'program')
    ordering = ('user',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'full_name', 'mobile', 'country', 'guardian_contact')
    search_fields = ('full_name', 'student__user__username', 'country')
    list_filter = ('country',)
    ordering = ('full_name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'code', 'credit_hours')
    search_fields = ('name', 'code', 'program__name')
    list_filter = ('program',)
    ordering = ('name',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'year', 'grade')
    search_fields = ('student__user__username', 'course__name', 'semester', 'year')
    list_filter = ('semester', 'year', 'grade', 'course')
    ordering = ('student',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'latitude', 'longitude', 'duration', 'created_at')
    search_fields = ('student__user__username',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'status', 'created_at')
    search_fields = ('attendance__student__user__username',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('student', 'incident_date', 'description')
    search_fields = ('student__user__username', 'incident_date')
    list_filter = ('incident_date',)
    ordering = ('-incident_date',)


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('leave_type', 'student', 'start_date', 'end_date', 'reason', 'approval_status')
    search_fields = ('student__user__username', 'leave_type__title', 'approval_status')
    list_filter = ('approval_status', 'start_date', 'end_date')
    ordering = ('-start_date',)
