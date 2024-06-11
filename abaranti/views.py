from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Patient, Medicine, Treatment
from django.http import HttpResponse


# Index view
def index(request):
    return render(request, 'index.html')


# List view for patients
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


# Detail view for a patient
def patient_detail(request, pat_id):
    patient = get_object_or_404(Patient, pat_id=pat_id)
    return render(request, 'patient_detail.html', {'patient': patient})


# Create a new patient
def patient_create(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        insurance_number = request.POST.get('insurance_number')
        insurance_expiry_date = request.POST.get('insurance_expiry_date')
        Patient.objects.create(first_name=first_name, last_name=last_name, insurance_number=insurance_number,
                               insurance_expiry_date=insurance_expiry_date)
        return redirect('patient_list')
    return render(request, 'patient_form.html')


# Update an existing patient
def patient_update(request, pat_id):
    patient = get_object_or_404(Patient, pat_id=pat_id)
    if request.method == 'POST':
        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.insurance_number = request.POST.get('insurance_number')
        patient.insurance_expiry_date = request.POST.get('insurance_expiry_date')
        patient.save()
        return redirect('patient_detail', pat_id=patient.pat_id)
    return render(request, 'patient_form.html', {'patient': patient})


# Delete a patient
def patient_delete(request, pat_id):
    patient = get_object_or_404(Patient, pat_id=pat_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patient_confirm_delete.html', {'patient': patient})
