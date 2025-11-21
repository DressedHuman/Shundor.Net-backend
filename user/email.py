"""
Custom email classes for user-related notifications.
"""
from djoser import email

class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = "email/password_reset.html"





