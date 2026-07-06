from django import forms
from .models import Appointment, MedicalRecord
from django.utils.translation import gettext_lazy as _

class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason_for_visit']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason_for_visit': forms.Textarea(attrs={'rows': 4}),
        }
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time', 'reason_for_visit', 'status']
        widgets = {
            'patient': forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__name='Patient')), # not intuitive
            'doctor': forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__name='Doctor')),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason_for_visit': forms.Textarea(attrs={'rows': 4}),
            'status': forms.Select(),
        }
        
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'record']
        widgets = {
            'record': forms.Textarea(attrs={'rows': 4}),
        }
        
