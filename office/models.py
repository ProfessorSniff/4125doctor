from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments', limit_choices_to=Q(groups__name='Patient'))
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to=Q(groups__name='Doctor'), blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True)
    
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