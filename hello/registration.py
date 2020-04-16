import os

from django.shortcuts import render
from .db import myDB
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import argon2

class PasswordChangeForm(forms.ModelForm):
    validatePass = RegexValidator(r'^(?=.*\d)(?=.*[a-z])(?=.*[\W]).{8,20}',
                                  'Password does not meet complexity requirement.')
    confirmPass = RegexValidator(r'^(?=.*\d)(?=.*[a-z])(?=.*[\W]).{8,20}', 'Passwords do not match')
    pword = forms.CharField(label='Password' ,max_length=20, min_length=8, required=True, widget=forms.PasswordInput,
                            validators=[validatePass],
                            help_text='<br><i>Password must be: <br>- Between 8-20 characters<br>- Must have one small alphabet<br>- Must have one capital alphanet<br>- Must have one number<br>- Must have one special character</i>')
    confirm_password = forms.CharField(label='Confirm Password', max_length=20, min_length=8, required=True, widget=forms.PasswordInput,
                                       validators=[confirmPass])

    class Meta:
        model = User
        fields = ['pword', 'confirm_password']


def PasswordResetView(request):
    message = ""
    return render(request, "registration/reset_form.html", {"message": message})


def reset(request):
    email = str(request.POST['email']).lower()
    id_user = str(request.POST['id_user']).lower()
    conn = myDB.connect()
    cursor = conn.cursor()

    cursor.execute("""SELECT id FROM users WHERE uname=%(u_name)s AND email=%(email)s""", {'u_name':id_user, 'email': email})
    u_id = cursor.fetchone()
    cursor.close()
    conn.close()
    validity = True
    if u_id is not None:
        validity = True
        message = "Matching email found."
        form = PasswordChangeForm(request.POST)
        return render(request, "registration/change_form.html", {"message": message, "validity": validity, 'form': form, 'u_id': u_id[0]})
    message = "Matching email not found"
    return render(request, "registration/reset_form.html", {"message": message, })


def change(request):
    u_id = (request.POST['u_id'])
    user_id = int(u_id)
    pword = str(request.POST['pword'])


    conn = myDB.connect()
    cursor = conn.cursor()

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
    hash = argon2Hasher.hash(pword)

    try:
        cursor.execute("""UPDATE users SET pword=%(hash)s WHERE id=%(user_id)s""",
                    {'hash': hash, 'user_id':user_id})
        conn.commit()
        result = True
    except:
        pass
    finally:
        cursor.close
        conn.commit()

    if result:
        message = "Password changed successfully."
        return render(request, "registration/change_confirm.html", {"message": message})
    else:
        message = "Error! Failed to change password."

    return render(request, "registration/reset_form.html", {"message": message, })



