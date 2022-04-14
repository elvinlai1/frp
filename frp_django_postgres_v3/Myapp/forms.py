from django import forms
from django.forms import ModelForm
from Myapp.models.employees import Employees


class NewUserForm(ModelForm):

	class Meta:
		model = Employees
		fields = ("employee_number", "employee_name", "department")

	def save(self, commit=True):
		Employees = super(NewUserForm, self).save(commit=False)
		if commit:
			Employees.save()
		return Employees