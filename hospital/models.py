from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    disease = models.CharField(max_length=200)
    doctor = models.CharField(max_length=200)
    admitted_on = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Active', 'Active'), ('Discharged', 'Discharged'), ('Critical', 'Critical')],
        default='Active'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-admitted_on']


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Appointment(models.Model):
    patient_name = models.CharField(max_length=200)
    doctor_name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Scheduled'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name} on {self.date}"

    class Meta:
        ordering = ['date']
