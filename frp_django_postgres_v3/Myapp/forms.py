from django import forms
from django.forms import ModelForm
from Myapp.models.race_user import User


class NewUserForm(ModelForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("first_name","last_name", "email", "department", "wage_per_hour")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user