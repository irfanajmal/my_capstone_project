import datetime
import subprocess
import time
import pytz
from django.utils import timezone
import glob
import argon2
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from .db import myDB
import cryptography
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class UserLoginForm(forms.Form):
    validateUser = RegexValidator(r'^[0-9a-zA-Z@-_.]*$', 'Invalid user name!')
    User_Name = forms.CharField(max_length=10, min_length=3, required=True, validators=[validateUser])
    Password = forms.CharField(max_length=16, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['User_Name', 'Password']


class NewForm(forms.Form):
    validateUser = RegexValidator(r'^[0-9a-zA-Z@-_.]*$', 'Invalid user name!')
    To = forms.CharField(required=False, max_length=20, label='Send To', validators=[validateUser])
    Message = forms.CharField(required=False, max_length=10000, widget=forms.Textarea, label='Message',
                              validators=[validateUser])


class MySession:
    conn = myDB.connect()
    cursor = conn.cursor()

    @staticmethod
    def set(username, expiry_minutes) -> object:
        if expiry_minutes is None:
            exp_time = (datetime.datetime.now() + datetime.timedelta(minutes=10))
        else:
            exp_time = (datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes))
        expiry = exp_time.strftime("%Y-%b-%d %H:%M:%S")
        session_id = str(os.urandom(16).hex())
        sql = "INSERT INTO auth_session (username, session_id, expiry) VALUES (%s, %s, %s)"
        val = (username, session_id, expiry)
        MySession.cursor.execute(sql, val)
        # MySession.conn.commit()
        MySession.purge()
        return True

    @staticmethod
    def get(username):
        MySession.purge()
        result = MySession.cursor.execute("""SELECT MAX(expiry) FROM auth_session WHERE username = %(username)s""",
                                          {'username': username})
        result = MySession.cursor.fetchone()[0]
        if result is None:
            return False
        return True

    @staticmethod
    def getid(username):
        MySession.cursor.execute("""SELECT id FROM users WHERE uname = %(username)s""",
                                 {'username': username})
        uid = MySession.cursor.fetchone()
        return uid[0]

    @staticmethod
    def purge():
        exp_time = (datetime.datetime.now())
        now = exp_time.strftime("%Y-%b-%d %H:%M:%S")
        MySession.cursor.execute("""DELETE FROM auth_session WHERE expiry < %(now)s""", {'now': now})
        MySession.conn.commit()

    @staticmethod
    def clear(username):
        MySession.cursor.execute("""DELETE FROM auth_session WHERE username = %(username)s""",
                                 {'username': username})
        MySession.conn.commit()
        return "User Logged out."


def tz_test(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'tz_test.html', {'timezones': pytz.all_timezones})

    return render(request, 'tz_test.html', {'var': var,})

def index(request):
    submitted = False
    message = " "
    # IF FORM SUBMISSION IS PORT
    if request.method == 'POST':
        # IF SESSION IS VALID
        try:
            username = str(request.POST['User_Name']).lower()
        except:
            username = ""
        try:
            submitted = request.POST['submitted']
        except:
            submitted = False

        if MySession.get(username):
            # IF THERE IS AN ACTION
            try:
                action = request.POST['action']
            except:
                action = ""
            # IF ACTION IS SEND NEW MESSAGE
            if action == "send_new_message":
                message = send(request)
                uid = MySession.getid(request.POST['User_Name'])
                inbox_objects = inbox(request, request.POST['User_Name'], uid, message)
                return render(request, "messages.html", inbox_objects)
            # IF ACTION IS LOGOUT
            elif action == "logout":
                logout(request)
                request.close()
            # IF ACTION IS REFRESH OR LOAD NEW PAGE
            else:
                # message = request.POST['message']
                uid = MySession.getid(request.POST['User_Name'])
                inbox_objects = inbox(request, request.POST['User_Name'], uid, message)
                return render(request, "messages.html", inbox_objects)
        # IF SESSION IS NOT VALID AND USERNAME IS IN PORT
        elif username is not "" and not submitted:
            message = message + "Session Expired for " + username
            login(request, message)
            request.close()
        # IF SESSION IS NOT VALID AND NO USER IN POST THEN NEW LOGIN
        else:
            # form = UserLoginForm(request.POST)
            obj = login(request, message, )
            if obj is not None:
                return render(obj[0], obj[1], obj[2])
            else:
                message = "Error! User Authentication Failed."
    else:
        login(request, message)
    form = UserLoginForm()
    return render(request, 'index.html', {'submitted': submitted, 'form': form, 'message': message})


def login(request, message):
    form = UserLoginForm(request.POST)
    submitted = False
    if form.is_valid():
        cd = form.cleaned_data
        authenticated = user_auth(cd, request)
        if not authenticated[0]:
            message = "Error!: Failed to Authenticate the user."
            submitted = False
        else:
            submitted = True
            MySession.set(authenticated[1], 10)
            inbox_objects = inbox(request, authenticated[1], authenticated[2], message)
            return request, "messages.html", inbox_objects
    else:
        submitted = True
    # message = message + " M:login:1:"
    # return render(request, "index.html", {'submitted': submitted, 'form': form, 'message': message})


def logout(request):
    message = MySession.clear(request.POST['User_Name'])
    form = UserLoginForm()
    submitted = False
    message = "User_Logedout"
    request.close()
    return render(request, "index.html", {'submitted': submitted, 'form': form, 'message': message})


def inbox(request, username, user_id, message):
    msgs_date = get_messages(username)
    from_msgs = msgs_date[0]
    to_msgs = msgs_date[1]
    new_usr_form = NewForm()
    message = message
    return {'user_name': username, "uid": user_id, 'message': message, 'from_msgs': from_msgs,
            'to_msgs': to_msgs, 'new_usr_form': new_usr_form}


def register(request):
    message = ""
    return render(request, "register.html", {"message": message})


def db(request):
    exp_time = (datetime.datetime.utcnow())
    time_now = exp_time.strftime("%d_%m_%Y-%H%M%S-%f")
    db_file_name = ""
    db_path_file = ""
    try:
        submitted1 = request.POST['submitted']
    except:
        submitted1 = False
    try:
        db_file_name = request.POST['db_file_name']
    except:
        db_file_name = ""
    try:
        generated_on = str(request.POST['generated_on'])
    except:
        generated_on = ""

    if request.method == 'POST' and submitted1 and not (submitted1 and db_file_name != ""):
        if submitted1:
            files = glob.glob('dbdump/Heroku_Postgres_DB*')
            seconds = time.time() - (5 * 60)
            for f in files:
                try:
                    if seconds >= os.stat(f).st_ctime:
                        os.remove(f)
                except:
                    do_nothing = ""
            files = glob.glob('dbdump/Heroku_Postgres_DB*')
            db_file_name = "Heroku_Postgres_DBDUMP_" + time_now + ".sql"
            if len(files) == 0:
                pg_dump = subprocess.Popen(['pg_dump',
                                            'postgres://rsbuhqmqigficf:652bd8fc4f26892df10cc924568a9698c53503351a202159356cc4f3292a962c@ec2-52-86-33-50.compute-1.amazonaws.com:5432/d8r5bdme8ltj0g'],
                                           stdout=subprocess.PIPE, universal_newlines=True)
                output = pg_dump.stdout.read()
                db_file_name = "Heroku_Postgres_DB_" + time_now + ".sql"
                # db_file_name = "Heroku_Postgres_DB.sql"
                db_path_file = "dbdump/" + db_file_name
                File1 = open(db_path_file, "w")
                File1.write(output)
                File1. close()
                return FileResponse(open(db_path_file,'rb'))
            else:
                return FileResponse(open(files[0], 'rb'))

    submitted2 = False
    return render(request, "db.html", {'db_file_name': db_file_name, 'submitted': submitted2})


def user_auth(cd, request) -> object:
    user_name = str(cd['User_Name']).lower()
    User_password = cd['Password']

    conn = myDB.connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT pword, id FROM users WHERE uname = %(username)s""", {'username': user_name})
    my_hash = cursor.fetchone()
    cursor.close()
    conn.close()

    argon2_hashed = argon2.PasswordHasher(time_cost=16, memory_cost=2 ** 15, parallelism=2, hash_len=32, salt_len=16)

    result = True
    try:
        verifyValid = argon2_hashed.verify(my_hash[0], User_password)
    except:
        result = False
        return result, '', ''
    return result, user_name, my_hash[1]


def get_messages(username):
    d_from_msgs = []
    d_to_msgs = []
    conn = myDB.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT from_usr, encode(messages.bmessage, 'hex'), msg_time  FROM messages WHERE to_usr = %(username)s""",
                       {'username': username})
        from_msgs = cursor.fetchall()
        cursor.execute("""SELECT to_usr, encode(messages.bmessage, 'hex'), msg_time FROM messages WHERE from_usr = %(username)s""",
                       {'username': username})
        to_msgs = cursor.fetchall()
        cursor.execute("""SELECT timezone FROM users WHERE uname = %(username)s""", {'username': username})
        tz_t = cursor.fetchone()
        tz = str(tz_t[0])
        time_zone = pytz.timezone(tz)

        _d_from_msgs = []
        _d_to_msgs = []

        i = 0
        for msg in from_msgs:
            if from_msgs[i][1] is not None:
                dec_msg = msg_decode(msg[1], msg[0])
                _d_from_msgs = list(msg)
                _d_from_msgs[1] = dec_msg
                utc_naive = _d_from_msgs[2].replace(tzinfo=pytz.utc)
                localDatetime = utc_naive.astimezone(time_zone)
                _d_from_msgs[2] = localDatetime
            i += 1
            d_from_msgs.append(_d_from_msgs)

        i = 0
        for msg in to_msgs:
            if to_msgs[i][1] is not None:
                dec_msg = msg_decode(msg[1], username)
                _d_to_msgs = list(msg)
                _d_to_msgs[1] = dec_msg
                utc_naive = _d_to_msgs[2].replace(tzinfo=pytz.utc)
                localDatetime = utc_naive.astimezone(time_zone)
                _d_to_msgs[2] = localDatetime
            d_to_msgs.append(_d_to_msgs)
            i += 1

    except Exception as e:
        print ("Error while getting data from PostgreSQL", e)
    finally:
        if(conn):
            cursor.close()
            conn.close()
    return d_from_msgs, d_to_msgs


def send(request):
    user_name = request.POST['User_Name']
    to_user = str(request.POST['To']).lower()
    msg = request.POST['Message']
    enc_msg = msg_encode(msg, user_name)
    now = time.strftime("%a, %d %b %y %H:%M:%S.%s")
    conn = myDB.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT id FROM users WHERE uname = %(username)s""",
                       {'username': to_user})
        check_user = cursor.fetchone()
    except:
        pass
    if check_user is None:
        message = "Error! " + to_user + " was not found."
        return message

    sql = "INSERT INTO messages (from_usr, to_usr, bmessage, msg_time) VALUES (%s, %s, %s, %s)"
    val = (user_name, to_user, enc_msg, now)
    try:
        cursor.execute(sql, val)
    except:
        success = False
        conn.commit()
        cursor.close()
        conn.close()
        message = "Message not sent"
        return message
    success = True
    conn.commit()
    cursor.close()
    conn.close()
    submitted = True
    message = "Message sent"
    return message


def msg_decode(enmessage, username):
    conn = myDB.connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT encode(users.hash, 'hex') FROM users WHERE uname = %(username)s""", {'username': username})
    hex_hash = cursor.fetchone()
    key = bytes.fromhex(hex_hash[0])
    cursor.close()
    conn.close()
    f = Fernet(key)
    byte_message = bytes.fromhex(enmessage)
    msg = f.decrypt(byte_message)
    return msg.decode()


def msg_encode(message, username):
    conn = myDB.connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT encode(users.hash, 'hex') FROM users WHERE uname = %(username)s""", {'username': username})
    hex_hash = cursor.fetchone()
    key = bytes.fromhex(hex_hash[0])
    cursor.close()
    conn.close()
    f = Fernet(key)
    enm = f.encrypt(message.encode())
    return enm


def gen_key_m(my_hash):
    password_provided = str(my_hash)
    password = password_provided.encode()
    salt = b'\xea\xbf\xbb\xac{\xc5\xaa\xf0)\x05\x93cXjI\x93'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

