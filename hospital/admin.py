from django.contrib import admin
from .models import Patient, Doctor, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'disease', 'doctor', 'status', 'admitted_on']
    list_filter = ['status']
    search_fields = ['name', 'disease', 'doctor']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'phone', 'available']
    list_filter = ['available', 'specialization']
    search_fields = ['name', 'specialization']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor_name', 'date', 'time', 'status']
    list_filter = ['status', 'date']
    search_fields = ['patient_name', 'doctor_name']
