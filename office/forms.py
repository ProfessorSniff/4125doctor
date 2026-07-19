from django import forms
from .models import Appointment, MedicalRecord, validate_appointment_attachment
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import os

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time', 'reason', 'attachment', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
            'attachment': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png,.webp,.gif,.bmp,.tiff'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This is apparently the best way to limit selection to patients and doctors
        self.fields['patient'].queryset = User.objects.filter(groups__name='Patient')
        self.fields['doctor'].queryset = User.objects.filter(groups__name='Doctor')
    
    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            validate_appointment_attachment(attachment)
        return attachment    

class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason', 'attachment']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
            'attachment': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png,.webp,.gif,.bmp,.tiff'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(groups__name='Doctor')
    
    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            validate_appointment_attachment(attachment)
        return attachment
        
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'record']
        widgets = {
            'record': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = User.objects.filter(groups__name='Patient')