from django.shortcuts import render
from django.http import HttpResponse
import requests
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .db import myDB
import pandas as pd


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

	return render(request, 'index.html', {'form': form, 'submitted': submitted} )


def register(request):
	return render(request, "register.html", {"message": message})

def db(request):
	conn = myDB.connect()
	cursor = conn.cursor()
	query = "SELECT * FROM users;"
	cursor.execute(query)
	info = cursor.fetchall()

	df = pd.DataFrame(data=info)
	df_html = df.to_html()

	return render(request, "db.html", {"greetings": df_html})





