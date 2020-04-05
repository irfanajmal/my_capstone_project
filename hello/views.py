from django.shortcuts import render
from django.http import HttpResponse
import requests
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .db import myDB
import pandas as pd
import hashlib
import sys
import random
import os
import argon2, binascii


class UserLoginForm(forms.Form):

	validateUser = RegexValidator(r'^[0-9a-zA-Z@-_.]*$', 'Invalid user name!')
	User_Name = forms.CharField(max_length=10, min_length=3, required=True, validators=[validateUser] )
	Password = forms.CharField(max_length=16, required=True, widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['User_Name', 'Password']

def index(request):
	submitted = False
	message = " "
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			authenticated = userAuth(cd, request)
			if not authenticated:
				message = "Error: User name or password are incorrect!"
				submitted = False
	else:
		form = UserLoginForm()
		if 'submitted' in request.GET:
			submitted = True

	return render(request, "index.html", {'submitted': submitted, 'form': form, 'message': message })


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

	return render(request, "db.html", {"df_html": df_html})

def userAuth(cd, request):
	uname=cd['User_Name']
	pword=cd['Password']

	conn = myDB.connect()
	cursor = conn.cursor()
	cursor.execute("""SELECT pword FROM users WHERE uname = %(username)s""", {'username': uname })
	hash = cursor.fetchone()

	argon2Hasher = argon2.PasswordHasher(time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)

	try:
		verifyValid = argon2Hasher.verify(hash[0], pword)
	except:
		result = False
	else:
		result = True
		return render(request, "db.html", {"uname": uname})
	return result
