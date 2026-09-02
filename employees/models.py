from django.db import models

# Create your models here.
class Employee(models.Model):
    emp_id = models.CharField(max_length= 20, unique = True, verbose_name = "Employee ID")
    name = models.CharField(max_length = 100, verbose_name ="Employee Name")
    email = models.EmailField(unique= True, verbose_name = "Email Address")
    phone = models.CharField(max_length = 15, verbose_name = "Phone Number")
    department = models.CharField(max_length = 100, verbose_name = "Department")
    designation = models.CharField(max_length=100, verbose_name="Designation")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salary")
    joining_date = models.DateField(verbose_name="Joining Date")
    def __str__(self):
        return f"{self.emp_id} - {self.name}"
     