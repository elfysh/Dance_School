from datetime import datetime, UTC, timedelta

import jwt
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app import models
from app.views.helper import check_jwt
from sports_booking import settings


def admin(request):
    return check_jwt(request, render(request, "admin/admin_panel.html"))


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = models.AdminUser.objects.filter(username=username, password=password).first()
        if user is not None:
            payload = {
                "user_id": user.id,
                "username": user.username,
                "exp": datetime.now(UTC) + timedelta(minutes=15)
            }
            token = jwt.encode(payload, settings.SECRET_KEY_ADMIN, algorithm='HS256')
            response = redirect('/admin/')
            response.set_cookie('access_token', str(token), httponly=True)
            response.set_cookie('refresh_token', str(token), httponly=True)
            print(token)
            print("User is found")
            return response
        else:
            return render(request, "admin/admin_login.html", {"error": "Неверное имя пользователя или пароль"})
    return render(request, "admin/admin_login.html")

'''
API v1
'''

@csrf_exempt
def api_admin_login(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = models.AdminUser.objects.filter(username=username, password=password).first()
    if user is not None:
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.now(UTC) + timedelta(minutes=15)
        }
        token = jwt.encode(payload, settings.SECRET_KEY_ADMIN, algorithm='HS256')
        resp = HttpResponse(status=200)
        resp.headers['Token'] = token
        return resp
    else:
        return HttpResponse(status=401)
