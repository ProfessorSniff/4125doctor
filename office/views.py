from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Appointment, MedicalRecord
from .forms import AppointmentForm, PatientAppointmentForm, MedicalRecordForm

# Create your views here.

# read

@login_required
def dashboard_patient(request):
    patient_appointments = request.user.appointments.all()
    patient_medical_records = request.user.medical_records.all()
    
    return render(request, 'office/dashboard_patient.html', {
        'patient_appointments': patient_appointments,
        'patient_medical_records': patient_medical_records
    })
    
@login_required
@user_passes_test(is_doctor, login_url='/unauthorized/')
def dashboard_doctor(request):
    doctor_appointments = request.user.doctor_appointments.all()
    doctor_medical_records = request.user.doctor_medical_records.all()
    
    return render(request, 'office/dashboard_doctor.html', {
        'doctor_appointments': doctor_appointments,
        'doctor_medical_records': doctor_medical_records
    })

@login_required
@user_passes_test(is_doctor, login_url='/unauthorized/')
def list_appointments_office(request):
    appointments = Appointment.objects.all()
    return render(request, 'office/list_appointments_office.html', {'appointments': appointments})

# create

@login_required
def book_appointment(request):
    if request.method != 'POST':
        form = PatientAppointmentForm()
    else: # submitted form
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False) # modify without really saving
            appointment.patient = request.user
            appointment.save()
            return redirect('dashboard_patient')
    
    return render(request, 'office/create_appointment.html', {'form': form})

@login_required
@user_passes_test(is_doctor, login_url='/unauthorized/')
def create_appointment(request):
    if request.method != 'POST':
        form = AppointmentForm()
    else: # submitted form
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_doctor')
    return render(request, 'office/create_appointment.html', {'form': form})

@login_required
@user_passes_test(is_doctor, login_url='/unauthorized/')
def create_medical_record(request):
    if request.method != 'POST':
        form = MedicalRecordForm()
    else: # submitted form
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.doctor = request.user
            medical_record.save()
            return redirect('dashboard_doctor')
    return render(request, 'office/create_update_medical_record.html', {'form': form})

# update

@login_required
@user_passes_test(is_doctor, login_url='/unauthorized/')
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method != 'POST':
        form = AppointmentForm(instance=appointment)
    else: # submitted form
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('dashboard_doctor')
    
    return render(request, 'office/update_appointment.html', {'form': form, 'appointment': appointment})

@login_required
@user_passes_test(is_doctor, login_url='/unauthorized/')
def update_medical_record(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    if request.method != 'POST':
        form = MedicalRecordForm(instance=record)
    else:
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard_doctor')
    return render(request, 'office/create_update_medical_record.html', {'form': form, 'record': record})