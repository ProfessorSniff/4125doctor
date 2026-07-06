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
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
        if self.groups.filter(name='Patient').exists() and self.groups.filter(name='Doctor').exists():
            raise ValidationError(_('A user cannot be both a patient and a doctor.'))

        if self.groups.count() == 0:
            raise ValidationError(_('A user must belong to at least one group (Patient or Doctor).'))
    
    # role helpers
    
    @property
    def is_patient(self):
        return self.groups.filter(name='Patient').exists() or self.is_superuser
    
    @property
    def is_doctor(self):
        return self.groups.filter(name='Doctor').exists() or self.is_superuser
    
    @property
    def display_name(self):
        # not sure if this is really smart or really not
        return " ".join(filter(None, [self.first_name, self.last_name])) or self.username 