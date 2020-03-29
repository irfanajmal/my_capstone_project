from django.shortcuts import render
from django.http import HttpResponse
import requests

from .models import Greeting

# Create your views here.
def index(request):
	return render(request, "index.html")

def register(request):
	message = "Hello"
	if request.method == 'POST':
		message = "Hello world!"
		return render(request, "register.html", {"message": message})
	return render(request, "register.html", {"message": message})

def db(request):

	greeting = Greeting()
	greeting.save()
	greetings = Greeting.objects.all()
	return render(request, "db.html", {"greetings": greetings})


def submit(request):
	return HttpResponse('Hello world')

def username_check(username): 
      
	reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[._-])[A-Za-z\d._-]{4,10}$"
	val = True
      
	pat = re.compile(reg) 
      
	mat = re.search(pat, passwd) 
      
	if mat: 
		return ("Invalid user name!") 
	else: 
		return ("Valid user name!") 


def password_check(passwd): 
      
	reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
	pat = re.compile(reg) 
	mat = re.search(pat, passwd) 
      
	if mat: 
		return ("Invalid password!") 
	else: 
		return ("Valid pasword!")  


