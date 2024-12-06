import hashlib
from datetime import datetime, UTC, timedelta

import jwt
import requests
from django.shortcuts import redirect, render

from app import models
from sports_booking import settings


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode(), usedforsecurity=True).hexdigest()
        user = models.Client.objects.filter(name=username, password=hashed_password).first()
        if user is not None:
            payload = {
                "user_id": user.client_id,
                "username": user.name,
                "exp": datetime.now(UTC) + timedelta(minutes=15)
            }
            token = jwt.encode(payload, settings.SECRET_KEY_USER, algorithm='HS256')
            response = redirect('/user/')
            response.set_cookie('access_token', str(token), httponly=True)
            response.set_cookie('refresh_token', str(token), httponly=True)
            print(token)
            print("User is found")
            return response
        else:
            return render(request, "user/user_login.html", {"error": "Неверное имя пользователя или пароль"})
    return render(request, "user/user_login.html")

def user_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        phone = request.POST.get('phone')
        user = models.Client.objects.filter(name=username).first()
        if user is not None:
            return render(request, "user/user.html", {"error": "Пользователь с таким именем уже существует"})
        elif password != password_repeat:
            return render(request, "user/user.html", {"error": "Пароли не совпадают"})
        else:
            hash_password = hashlib.sha256(password.encode(), usedforsecurity=True).hexdigest()
            models.Client.objects.create(
                name=username,
                password=hash_password,
                phone_number=phone
            )
            # Send post request /user/login
            return requests.post("http://127.0.0.1/user/login", data={"username": username, "password": password})
