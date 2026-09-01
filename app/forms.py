import re
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'emp_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., EMP101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Phone Number'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Engineering'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Software Engineer'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50000.00'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?[0-9]{10,15}$', phone):
            raise forms.ValidationError('Enter a valid phone number (10-15 digits).')
        return phone

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary <= 0:
            raise forms.ValidationError('Salary must be a positive number.')
        return salary