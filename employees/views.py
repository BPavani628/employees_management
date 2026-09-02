

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Sum, Avg
from .models import Employee
from .forms import EmployeeForm

# ----------------- AUTHENTICATION VIEWS ----------------- #

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'employees/login.html', {'form': form})


def admin_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ----------------- DASHBOARD & CRUD VIEWS ----------------- #

@login_required(login_url='login')
def dashboard(request):
    total_employees = Employee.objects.count()
    total_salary = Employee.objects.aggregate(Sum('salary'))['salary__sum'] or 0
    avg_salary = Employee.objects.aggregate(Avg('salary'))['salary__avg'] or 0
    recent_employees = Employee.objects.all().order_by('-id')[:5]

    context = {
        'total_employees': total_employees,
        'total_salary': total_salary,
        'avg_salary': avg_salary,
        'recent_employees': recent_employees,
    }
    return render(request, 'employees/dashboard.html', context)


@login_required(login_url='login')
def employee_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        employees = Employee.objects.filter(
            Q(name__icontains=query) | Q(emp_id__icontains=query)
        )
    else:
        employees = Employee.objects.all()

    return render(request, 'employees/employee_list.html', {'employees': employees, 'query': query})


@login_required(login_url='login')
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required(login_url='login')
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add New Employee'})


@login_required(login_url='login')
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee details updated successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee Details'})


@login_required(login_url='login')
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee record deleted successfully!")
        return redirect('employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})