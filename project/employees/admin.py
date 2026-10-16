from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'department', 'designation', 'salary', 'joining_date')
    search_fields = ('emp_id', 'name', 'department')
    list_filter = ('department', 'designation')