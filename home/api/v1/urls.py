from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.views import (
    SignupViewSet, LoginViewSet, StudentProfileViewSet,
    StudentViewSet, UniversityViewSet, CampusViewSet,
    DepartmentViewSet, ProgramViewSet, CourseViewSet,
    EnrollmentViewSet, AttendanceViewSet, AttendanceLogViewSet,
    DisciplineViewSet, LeaveTypeViewSet, LeaveViewSet, index, capture_image, StudentListViewSet
)
from home.models import AttendanceStatsView, StudentAttendanceStatsView

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("admin/student", StudentViewSet, basename="student")
router.register('studentprofile', StudentProfileViewSet, basename='studentprofile')
router.register('university', UniversityViewSet, basename='university')
router.register('campus', CampusViewSet, basename='campus')
router.register('department', DepartmentViewSet, basename='department')
router.register('program', ProgramViewSet, basename='program')
router.register('course', CourseViewSet, basename='course')
router.register('enrollment', EnrollmentViewSet, basename="enrollment")
router.register('attendance', AttendanceViewSet, basename="attendance")
router.register('attendancelog', AttendanceLogViewSet, basename="attendance_log")
router.register('discipline', DisciplineViewSet, basename="discipline")
router.register('leavetype', LeaveTypeViewSet, basename="leave_type")
router.register('leave', LeaveViewSet, basename="leave")
router.register('list_students', StudentListViewSet, basename="list_students")


urlpatterns = [
    path("", include(router.urls)),
    path('home', index, name='index'),
    path('capture/', capture_image, name='capture_image'),
    path('admin/attendance-stats/', AttendanceStatsView.as_view(), name='attendance-stats'),
    path('student/student-attendance-stats/<int:student_id>/', StudentAttendanceStatsView.as_view(), name='student-attendance-stats'),

]
