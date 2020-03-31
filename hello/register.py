from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.validators import RegexValidator


class UserRegistrationForm(forms.ModelForm):

	validateUser = RegexValidator(r'^[0-9a-zA-Z@-_.]*$', 'Only characters allowed: 0-9 a-z A-Z @ . - _')
	validatePass = RegexValidator(r'^(?=.*\d)(?=.*[a-z])(?=.*[\W]).{8,20}', 'Password does not meet complexity requirement.')
	confirmPass = RegexValidator(r'^(?=.*\d)(?=.*[a-z])(?=.*[\W]).{8,20}', 'Passwords do not match')	
	username = forms.CharField(max_length=10, min_length=3, required=True, validators=[validateUser] )
	password = forms.CharField(max_length=16, min_length=8, required=True, widget=forms.PasswordInput, validators=[validatePass] )
	confirm_password = forms.CharField(max_length=20, min_length=8, required=True, widget=forms.PasswordInput, validators=[confirmPass] )


	class Meta:
		model = User
		fields = ['username', 'password', 'password']
	

def register(request):
	submitted = False
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
						
			return HttpResponseRedirect('/register?submitted=True')
	else:
		form = UserRegistrationForm()
		if 'submitted' in request.GET:
			submitted = True
			
	return render(request, 'register.html', {'form': form, 'submitted': submitted})


