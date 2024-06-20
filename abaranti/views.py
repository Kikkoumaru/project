from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient, Employee
from django.contrib.auth.decorators import login_required, user_passes_test


def user_login(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        password = request.POST.get('password')
        user = authenticate(request, username=empid, password=password)  # empidをusernameに対応させる
        if user is not None:
            login(request, user)
            return redirect('patient_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid empid or password'})
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


def is_admin(user):
    return user.is_superuser  # 管理者かどうかを判定


@login_required(login_url='login')
def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, pat_id=patient_id)
    if request.method == "POST":
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patient_confirm_delete.html', {'patient': patient})


def register(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        password = request.POST.get('password')

        if empid and password:
            user = Employee.objects.create_user(empid=empid, password=password)
            return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'All fields are required'})
    return render(request, 'register.html')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')  # 管理者のみアクセス可能にする
def employee_register(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        empfname = request.POST.get('empfname')
        emplname = request.POST.get('emplname')
        password = request.POST.get('password')
        emprole = request.POST.get('emprole')

        if empid and empfname and emplname and password and emprole is not None:
            user = Employee.objects.create_user(empid=empid, empfname=empfname, emplname=emplname, password=password,
                                                emprole=emprole)
            return redirect('login')
        else:
            return render(request, 'employee_register.html', {'error': 'すべてのフィールドを入力してください。'})
    return render(request, 'employee_register.html')


def employee_search(request):
    if request.method == "POST":
        empid = request.POST.get('empid')
        try:
            employee = Employee.objects.get(empid=empid)
            return redirect('employee_update', pk=employee.pk)
        except Employee.DoesNotExist:
            return render(request, 'employee_search.html', {'error': '従業員が見つかりません'})
    return render(request, 'employee_search.html')


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        empid = request.POST.get('empid')
        empfname = request.POST.get('empfname')
        emplname = request.POST.get('emplname')
        emprole = request.POST.get('emprole')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        employee.empid = empid
        employee.empfname = empfname
        employee.emplname = emplname
        employee.emprole = emprole
        employee.is_staff = is_staff
        employee.is_superuser = is_superuser
        employee.save()

        return redirect('employee_search')
    return render(request, 'employee_update.html', {'employee': employee})
