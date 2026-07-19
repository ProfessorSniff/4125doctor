from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
import time
import os

APPOINTMENT_ALLOWED_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tiff']
APPOINTMENT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_appointment_attachment(file):
    if file.size > APPOINTMENT_MAX_FILE_SIZE:
        raise models.ValidationError(
            _('Max size: 10MB. Current size: %(size)s MB') % 
            {'size': round(file.size / (1024 * 1024), 2)}
        )
    
    ext = os.path.splitext(file.name)[1][1:].lower()
    if ext not in APPOINTMENT_ALLOWED_EXTENSIONS:
        raise models.ValidationError(
            _('File type ".%(ext)s" is not allowed. Allowed types: %(allowed)s') % 
            {'ext': ext, 'allowed': ', '.join(APPOINTMENT_ALLOWED_EXTENSIONS)}
        )


def appointment_attachment_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower() # built on the premise that the extension given by os.path is safe
    random_name = format(time.time_ns(), 'x')
    path = f"appointments/{random_name}{ext}"
    if os.path.exists(path):
        raise models.ValidationError(_('You are either uploading too fast or very unlucky. Please try again.'))
    return path

# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments', limit_choices_to=Q(groups__name='Patient'))
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to=Q(groups__name='Doctor'), blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True)
    attachment = models.FileField(
        upload_to=appointment_attachment_upload_to,
        blank=True,
        null=True,
        validators=[validate_appointment_attachment],
        help_text=_('Allowed file types: PDF, JPG, PNG, WebP, GIF, BMP, TIFF (Max 10MB)')
    )
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.patient.display_name} {_("with")} {self.doctor.display_name or _('(no doctor assigned)')}  {self.date_time.strftime('%F %T')}: {self.status}"
    
class MedicalRecord(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_medical_records', limit_choices_to=Q(groups__name='Doctor'))
    date_time = models.DateTimeField(auto_now_add=True)
    date_time_updated = models.DateTimeField(auto_now=True)
    record = models.TextField(blank=True)
    
    def __str__(self):
        return f"{_("Medical Record for")} {self.patient.display_name} {_("by")} {self.doctor.display_name or _('(no doctor assigned)')} {_("at")} {self.date_time.strftime('%F %T')}"