from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import StudentProfile, Student, Attendance, AttendanceLog


@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(student_id=instance.id, full_name=instance.user.name)
        print("Student profile is created!")
