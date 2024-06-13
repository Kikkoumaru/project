from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('patient_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


@login_required(login_url='login')
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, pat_id=patient_id)
    return render(request, 'patient_detail.html', {'patient': patient})


@login_required(login_url='login')
def patient_create(request):
    if request.method == "POST":
        pat_id = request.POST.get('pat_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        insurance_number = request.POST.get('insurance_number')
        insurance_expiry_date = request.POST.get('insurance_expiry_date')
        if pat_id and first_name and last_name and insurance_number and insurance_expiry_date:
            patient = Patient(pat_id=pat_id, first_name=first_name, last_name=last_name,
                              insurance_number=insurance_number, insurance_expiry_date=insurance_expiry_date)
            patient.save()
            return redirect('patient_list')
        else:
            return render(request, 'patient_form.html', {'error': 'All fields are required'})
    return render(request, 'patient_form.html')


@login_required(login_url='login')
def patient_update(request, patient_id):
    patient = get_object_or_404(Patient, pat_id=patient_id)
    if request.method == "POST":
        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.insurance_number = request.POST.get('insurance_number')
        patient.insurance_expiry_date = request.POST.get('insurance_expiry_date')
        if patient.first_name and patient.last_name and patient.insurance_number and patient.insurance_expiry_date:
            patient.save()
            return redirect('patient_list')
        else:
            return render(request, 'patient_form.html', {'patient': patient, 'error': 'All fields are required'})
    return render(request, 'patient_form.html', {'patient': patient})


@login_required(login_url='login')
def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, pat_id=patient_id)
    if request.method == "POST":
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patient_confirm_delete.html', {'patient': patient})
