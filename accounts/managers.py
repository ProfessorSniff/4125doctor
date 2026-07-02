from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)