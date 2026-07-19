"""
URL configuration for doctors_office_4125 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from office import views

from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),

    # Dashboards
    path('patient/dashboard/', views.dashboard_patient, name='dashboard_patient'),
    path('doctor/dashboard/', views.dashboard_doctor, name='dashboard_doctor'),

    # Appointments
    path('appointments/', views.list_appointments_office, name='list_appointments_office'),

    path('appointments/book/', views.book_appointment, name='book_appointment'),

    path('appointments/create/', views.create_appointment, name='create_appointment'),

    path(
        'appointments/<int:appointment_id>/update/',
        views.update_appointment,
        name='update_appointment'
    ),

    path(
        'appointments/<int:appointment_id>/attachment/delete/',
        views.delete_appointment_attachment,
        name='delete_appointment_attachment'
    ),

    # Medical Records
    path(
        'medical-records/create/',
        views.create_medical_record,
        name='create_medical_record'
    ),

    path(
        'medical-records/<int:record_id>/update/',
        views.update_medical_record,
        name='update_medical_record'
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]

# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)