from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    empid = models.CharField(max_length=8, primary_key=True, default='EMP0001')
    email = models.EmailField(unique=True, default='example@example.com')
    empfname = models.CharField(max_length=64, default='FirstName')  # デフォルト値を設定
    emplname = models.CharField(max_length=64, default='LastName')  # デフォルト値を設定
    emppasswd = models.CharField(max_length=256, default='password')  # デフォルト値を設定
    emprole = models.IntegerField(default=0)  # デフォルト値を設定 0: Receptionist, 1: Doctor

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['empfname', 'emplname']

    def __str__(self):
        return f"{self.empfname} {self.emplname}"


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
