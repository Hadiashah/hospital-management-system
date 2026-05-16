from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient, Doctor, Appointment
from .forms import PatientForm, DoctorForm, AppointmentForm
import datetime


# ─── AUTH VIEWS ────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'hospital/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# ─── DASHBOARD ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    active_patients = Patient.objects.filter(status='Active').count()
    critical_patients = Patient.objects.filter(status='Critical').count()
    today = datetime.date.today()
    todays_appointments = Appointment.objects.filter(date=today).count()
    upcoming_appointments = Appointment.objects.filter(date__gte=today, status='Scheduled').order_by('date')[:5]
    recent_patients = Patient.objects.order_by('-admitted_on')[:5]

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'active_patients': active_patients,
        'critical_patients': critical_patients,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'recent_patients': recent_patients,
        'today': today,
    }
    return render(request, 'hospital/dashboard.html', context)


# ─── PATIENT VIEWS ─────────────────────────────────────────────────────────────

@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(name__icontains=query) |
            Q(disease__icontains=query) |
            Q(doctor__icontains=query)
        )
    if status_filter:
        patients = patients.filter(status=status_filter)

    context = {
        'patients': patients,
        'query': query,
        'status_filter': status_filter,
        'total': patients.count(),
    }
    return render(request, 'hospital/patients.html', context)


@login_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient added successfully.')
            return redirect('patient_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PatientForm()
    return render(request, 'hospital/patient_form.html', {'form': form, 'action': 'Add Patient'})


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient "{patient.name}" updated successfully.')
            return redirect('patient_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/patient_form.html', {'form': form, 'action': 'Edit Patient', 'patient': patient})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        name = patient.name
        patient.delete()
        messages.success(request, f'Patient "{name}" deleted successfully.')
        return redirect('patient_list')
    return render(request, 'hospital/confirm_delete.html', {'object': patient, 'type': 'Patient'})


# ─── DOCTOR VIEWS ──────────────────────────────────────────────────────────────

@login_required
def doctor_list(request):
    query = request.GET.get('q', '')
    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) |
            Q(specialization__icontains=query)
        )

    context = {
        'doctors': doctors,
        'query': query,
        'total': doctors.count(),
    }
    return render(request, 'hospital/doctors.html', context)


@login_required
def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully.')
            return redirect('doctor_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DoctorForm()
    return render(request, 'hospital/doctor_form.html', {'form': form, 'action': 'Add Doctor'})


@login_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Dr. {doctor.name} updated successfully.')
            return redirect('doctor_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'hospital/doctor_form.html', {'form': form, 'action': 'Edit Doctor', 'doctor': doctor})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        name = doctor.name
        doctor.delete()
        messages.success(request, f'Dr. "{name}" deleted successfully.')
        return redirect('doctor_list')
    return render(request, 'hospital/confirm_delete.html', {'object': doctor, 'type': 'Doctor'})


# ─── APPOINTMENT VIEWS ─────────────────────────────────────────────────────────

@login_required
def appointment_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.all()

    if query:
        appointments = appointments.filter(
            Q(patient_name__icontains=query) |
            Q(doctor_name__icontains=query)
        )
    if status_filter:
        appointments = appointments.filter(status=status_filter)

    context = {
        'appointments': appointments,
        'query': query,
        'status_filter': status_filter,
        'total': appointments.count(),
    }
    return render(request, 'hospital/appointments.html', context)


@login_required
def appointment_add(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment scheduled successfully.')
            return redirect('appointment_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AppointmentForm()
    return render(request, 'hospital/appointment_form.html', {'form': form, 'action': 'Schedule Appointment'})


@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointment_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'hospital/appointment_form.html', {'form': form, 'action': 'Edit Appointment', 'appointment': appointment})


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
        return redirect('appointment_list')
    return render(request, 'hospital/confirm_delete.html', {'object': appointment, 'type': 'Appointment'})
