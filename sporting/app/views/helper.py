from datetime import datetime, timedelta, UTC

import jwt
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect

from sports_booking import settings


def check_jwt(
        request: WSGIRequest | str,
        content,
        secret_key=settings.SECRET_KEY_ADMIN,
        redirect_url='/admin/login'
):
    if type(request) == str:
        raw_token = request
    else:
        raw_token = request.COOKIES.get('access_token')
    if raw_token is None:
        return redirect(redirect_url)
    try:
        payload = jwt.decode(raw_token, secret_key, algorithms=['HS256'])
        print("Before: " + str(datetime.fromtimestamp(payload["exp"])))
        datetime.fromtimestamp(payload["exp"])
        payload["exp"] = datetime.now(UTC) + timedelta(minutes=15)
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        if type(content) == HttpResponse:
            content.set_cookie('access_token', str(token), httponly=True)
            content.set_cookie('refresh_token', str(token), httponly=True)
        print("After: " + str(payload["exp"]))
        return content
    except jwt.ExpiredSignatureError:
        print("Token is expired")
        return redirect(redirect_url)
    except jwt.InvalidTokenError:
        print("Invalid token")
        return redirect(redirect_url)