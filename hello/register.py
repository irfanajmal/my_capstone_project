from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

class UserRegistrationForm(forms.ModelForm):

	username = forms.CharField(max_length=10, required=True, )
	password = forms.CharField(max_length=16, required=True, )

	class Meta:
		model = User
		fields = ['username', 'password']

		widgets = {
			'password': forms.PasswordInput() 
		}


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


