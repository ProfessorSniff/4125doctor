from django import forms
from .models import Appointment, MedicalRecord
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time', 'reason', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This is apparently the best way to limit selection to patients and doctors
        self.fields['patient'].queryset = User.objects.filter(groups__name='Patient')
        self.fields['doctor'].queryset = User.objects.filter(groups__name='Doctor')    

class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(groups__name='Doctor')
        
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