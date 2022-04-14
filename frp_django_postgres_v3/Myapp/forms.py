from django import forms
from django.forms import ModelForm
from Myapp.models.employees import Employees
from Myapp.models.timestamps import Timestamps

class NewUserForm(ModelForm):

	class Meta:
		model = Employees
		fields = ("employee_number", "employee_name", "department")

	def save(self, commit=True):
		Employees = super(NewUserForm, self).save(commit=False)
		if commit:
			Employees.save()
		return Employees

class newTimestamp(ModelForm):
	class Meta:
		model = Timestamps
		fields = ("employee_number", "timestamp", "status")

	def save(self, commit=True):
		Timestamps = super(newTimestamp, self).save(commit=False)
		if commit: 
			Timestamps.save()
		return Timestamps
