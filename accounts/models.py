from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    # role helpers
    
    @property
    def is_patient(self):
        return self.groups.filter(name='Patient').exists()
    
    @property
    def is_doctor(self):
        return self.groups.filter(name='Doctor').exists()