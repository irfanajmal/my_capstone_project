import os
import time
import pytz
import argon2
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.shortcuts import render
from django.core.validators import validate_email
from .db import myDB
from .views import gen_key_m


class UserRegistrationForm(forms.ModelForm):
    validateUser = RegexValidator(r'^[0-9a-zA-Z@-_.]*$', 'Only characters allowed: 0-9 a-z A-Z @ . - _')
    validatePass = RegexValidator(r'^(?=.*\d)(?=.*[a-z])(?=.*[\W]).{8,20}',
                                  'Password does not meet complexity requirement.')
    confirmPass = RegexValidator(r'^(?=.*\d)(?=.*[a-z])(?=.*[\W]).{8,20}', 'Passwords do not match')
    uname = forms.CharField(label='User Name', max_length=10, min_length=3, required=True, validators=[validateUser],
                            help_text='<i>User name must be:<br>- 3 to 10 characters long.</i>')
    pword = forms.CharField(label='Password',max_length=20, min_length=8, required=True, widget=forms.PasswordInput,
                            validators=[validatePass],
                            help_text='<i>Password must be: <br>- Between 8-20 characters<br>- Must have one small alphabet<br>- Must have one capital alphanet<br>- Must have one number<br>- Must have one special character</i>')
    confirm_password = forms.CharField(label='Confirm Password', max_length=20, min_length=8, required=True, widget=forms.PasswordInput,
                                       validators=[confirmPass])
    email = forms.EmailField(label='Email Address',max_length=256,  required=True, validators=[validate_email], help_text='<i>Will be used for password retrieval.</i>')

    class Meta:
        model = User
        fields = ['uname', 'pword', 'confirm_password', 'email']


def signup(request):
    submitted = False
    message = ""
    try:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                timezone = request.POST['timezone']
                if create_user(cd, timezone):
                    submitted = True
                else:
                    submitted = False
                    message = "Error: User exists!"
        else:
            form = UserRegistrationForm()
    except Exception as e:
        message = e
        form = UserRegistrationForm()

    return render(request, 'signup.html', {'form': form, 'submitted': submitted, 'message': message, 'timezones': pytz.all_timezones, 'TIME_ZONE': "UTC"})


def create_user(cd, timezone):
    uname = str(cd['uname']).lower()
    pword = str(cd['pword'])
    email = str(cd['email']).lower()
    # now = time.localtime()
    now = time.strftime("%a, %d %b %y %H:%M:%S.%s")

    conn = myDB.connect()
    cursor = conn.cursor()

    sql = "SELECT id FROM users WHERE uname=%s and email=%s"
    val = (uname, email)
    cursor.execute(sql, val)
    rows = cursor.fetchone()

    if rows != None:
        result = False
    else:
        saltLen = 16
        hashLen = 32
        pword_salt = os.urandom(saltLen).hex()
        bpword_salt = bytes(pword_salt, encoding='utf-8')
        bpword = bytes(pword, encoding='utf-8')

        hash = argon2.hash_password_raw(
            time_cost=16, memory_cost=2 ** 15, parallelism=2, hash_len=hashLen,
            password=bpword, salt=bpword_salt, type=argon2.low_level.Type.ID)

        argon2Hasher = argon2.PasswordHasher(
            time_cost=16, memory_cost=2 ** 15, parallelism=2, hash_len=hashLen, salt_len=saltLen)
        hashed_pword = argon2Hasher.hash(pword)

        message_hash = gen_key_m(pword)

        sql = "INSERT INTO users (uname, email, pword, date_added, hash, timezone) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (uname, email, hashed_pword, now, message_hash, timezone)
        cursor.execute(sql, val)
        conn.commit()
        result = True
        cursor.close()
        conn.close()
        return result
