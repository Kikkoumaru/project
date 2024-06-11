from django.db import models

# Create your models here.
from django.db import models


class Employee(models.Model):
    emp_id = models.CharField(max_length=8, primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    role = models.IntegerField()  # 0: Receptionist, 1: Doctor


class Patient(models.Model):
    pat_id = models.CharField(max_length=8, primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    insurance_number = models.CharField(max_length=64)
    insurance_expiry_date = models.DateField()


class Medicine(models.Model):
    medicine_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)


class Treatment(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()
