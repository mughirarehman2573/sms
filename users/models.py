from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    choice = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    name = models.CharField(max_length=40, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=choice, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    face_encoding = models.ImageField(upload_to='user_images/', null=True, blank=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

#
# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens
#     When a token is created, an e-mail needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     # send an e-mail to the user
#     context = {
#         'current_user': reset_password_token.user,
#         'username': reset_password_token.user.username,
#         'email': reset_password_token.user.email,
#         'token': reset_password_token.key
#     }
#
#     # render email text
#     email_html_message = render_to_string('email/user_reset_password.html', context)
#     email_plaintext_message = render_to_string('email/user_reset_password.txt', context)
#
#     msg = EmailMultiAlternatives(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "support@portfolioguides.com",
#         # to:
#         [reset_password_token.user.email]
#     )
#     msg.attach_alternative(email_html_message, "text/html")
#     msg.send()
