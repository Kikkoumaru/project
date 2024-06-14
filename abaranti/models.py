from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, empid, password=None, **extra_fields):
        if not empid:
            raise ValueError('The Email field must be set')
        user = self.model(empid=empid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, empid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(empid, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    empid = models.CharField(max_length=8, primary_key=True, default='EMP0001')
    password = models.CharField(max_length=256, default='password')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'empid'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.empid


class Patient(models.Model):
    pat_id = models.CharField(max_length=8, primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    insurance_number = models.CharField(max_length=64)
    insurance_expiry_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Medicine(models.Model):
    medicine_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"Treatment {self.treatment_id} for {self.patient}"
