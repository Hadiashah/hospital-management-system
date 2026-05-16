#!/usr/bin/env python
"""
MediCore HMS — Quick Setup Script
Run this once after cloning/extracting the project.
"""
import os
import sys
import subprocess


def run(cmd, **kwargs):
    print(f"  → {cmd}")
    result = subprocess.run(cmd, shell=True, **kwargs)
    return result


def main():
    print("\n" + "═" * 55)
    print("  MediCore Hospital Management System — Setup")
    print("═" * 55 + "\n")

    # 1. Install Django
    print("📦 Installing dependencies...")
    run(f"{sys.executable} -m pip install Django>=4.2 --quiet")

    # 2. Run migrations
    print("\n🗄️  Running database migrations...")
    run(f"{sys.executable} manage.py makemigrations")
    run(f"{sys.executable} manage.py migrate")

    # 3. Create superuser
    print("\n👤 Creating default admin user...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_project.settings')

    import django
    django.setup()

    from django.contrib.auth.models import User
    from hospital.models import Patient, Doctor, Appointment
    import datetime

    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@medicore.com', 'admin123')
        print("  ✅ Admin user created: username=admin, password=admin123")
    else:
        print("  ℹ️  Admin user already exists.")

    # 4. Seed demo data
    print("\n🌱 Seeding demo data...")

    if Doctor.objects.count() == 0:
        doctors = [
            Doctor(name="Sarah Mitchell", specialization="Cardiologist", phone="+1-555-0101", email="s.mitchell@medicore.com", experience_years=12, available=True),
            Doctor(name="James Nguyen", specialization="Neurologist", phone="+1-555-0102", email="j.nguyen@medicore.com", experience_years=8, available=True),
            Doctor(name="Amelia Carter", specialization="Orthopedic Surgeon", phone="+1-555-0103", email="a.carter@medicore.com", experience_years=15, available=False),
            Doctor(name="David Okafor", specialization="General Practitioner", phone="+1-555-0104", email="d.okafor@medicore.com", experience_years=5, available=True),
        ]
        Doctor.objects.bulk_create(doctors)
        print(f"  ✅ Created {len(doctors)} doctors")

    if Patient.objects.count() == 0:
        patients = [
            Patient(name="Robert Johnson", age=54, disease="Hypertension", doctor="Dr. Sarah Mitchell", status="Active"),
            Patient(name="Maria Garcia", age=34, disease="Migraine", doctor="Dr. James Nguyen", status="Active"),
            Patient(name="Thomas Wilson", age=67, disease="Knee Replacement Recovery", doctor="Dr. Amelia Carter", status="Active"),
            Patient(name="Fatima Al-Hassan", age=28, disease="Common Cold", doctor="Dr. David Okafor", status="Discharged"),
            Patient(name="Kevin Park", age=45, disease="Chest Pain", doctor="Dr. Sarah Mitchell", status="Critical"),
        ]
        Patient.objects.bulk_create(patients)
        print(f"  ✅ Created {len(patients)} patients")

    if Appointment.objects.count() == 0:
        today = datetime.date.today()
        appointments = [
            Appointment(patient_name="Robert Johnson", doctor_name="Sarah Mitchell", date=today, time=datetime.time(9, 0), reason="Follow-up checkup", status="Scheduled"),
            Appointment(patient_name="Maria Garcia", doctor_name="James Nguyen", date=today, time=datetime.time(11, 30), reason="MRI review", status="Scheduled"),
            Appointment(patient_name="Kevin Park", doctor_name="Sarah Mitchell", date=today + datetime.timedelta(days=1), reason="Stress test", status="Scheduled"),
            Appointment(patient_name="Thomas Wilson", doctor_name="Amelia Carter", date=today + datetime.timedelta(days=3), time=datetime.time(14, 0), reason="Post-op evaluation", status="Scheduled"),
        ]
        Appointment.objects.bulk_create(appointments)
        print(f"  ✅ Created {len(appointments)} appointments")

    print("\n" + "═" * 55)
    print("  ✅ Setup complete! Ready to launch.")
    print("═" * 55)
    print("\n  Run the server with:")
    print("  python manage.py runserver")
    print("\n  Then open: http://127.0.0.1:8000")
    print("  Login:  admin / admin123\n")


if __name__ == '__main__':
    main()
