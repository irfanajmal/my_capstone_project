from django.shortcuts import render
from django.http import HttpResponse
import requests
from django import forms
from django.core.validators import RegexValidator
from .models import Greeting
from django.contrib.auth.models import User

class UserLoginForm(forms.ModelForm):

	validateUser = RegexValidator(r'^[0-9a-zA-Z@-_.]*$', 'Invalid user name!')
	username = forms.CharField(max_length=10, min_length=3, required=True, validators=[validateUser] )
	password = forms.CharField(max_length=16, min_length=8, required=True, widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'password']


def index(request):
	submitted = False
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			return HttpResponseRedirect('/register?submitted=True')
	else:
		form = UserLoginForm()
		if 'submitted' in request.GET:
			submitted = True
			
	return render(request, 'index.html', {'form': form, 'submitted': submitted})


def register(request):
	return render(request, "register.html", {"message": message})

def db(request):

	greeting = Greeting()
	greeting.save()
	greetings = Greeting.objects.all()
	return render(request, "db.html", {"greetings": greetings})

