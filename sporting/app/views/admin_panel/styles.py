from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app import models
from app.forms.style_forms import StyleForm
from app.views.helper import check_jwt


def admin_styles(request):
    if request.method == "GET":
        error_message = request.GET.get("error", "")
        styles = models.Style.objects.all()
        contents = {
            "styles": [],
            "error_message": error_message,
            "style_form": StyleForm(),
            "edit_style_form": StyleForm()
        }

        for style_id, style_name in styles.values_list("style_id", "style_name"):
            contents["styles"].append({"id": style_id, "name": style_name})

        contents["styles"].sort(key=lambda x: x["name"])

        return check_jwt(request, render(request, "admin/styles_list.html", contents))
    return redirect("/admin/styles?error=Неверный метод запроса", )


def add_style(request):
    if request.method == "POST":
        style_name = request.POST.get("style_name")
        check_result = check_jwt(request.COOKIES.get('access_token'), True)

        if type(check_result) != type(True):
            return redirect("/admin/login")

        style = models.Style.objects.filter(style_name=style_name).first()
        if style is None:
            models.Style.objects.create(style_name=style_name)
            return redirect("/admin/styles")
        else:
            return redirect("/admin/styles?error=Такой стиль уже существует", )
    return redirect("/admin/styles?error=Неверный метод запроса", )


def delete_style(request, _id: int):
    if request.method == "POST":
        check_result = check_jwt(request.COOKIES.get('access_token'), True)

        if type(check_result) != type(True):
            return redirect("/admin/login")

        style = models.Style.objects.filter(style_id=_id)
        if style is not None:
            style.delete()
            return redirect("/admin/styles")
        else:
            return redirect("/admin/styles?error=Такой стиль не существует", )
    return redirect("/admin/styles?error=Неверный метод запроса", )


def edit_style(request, _id: int):
    if request.method == "POST":
        new_name = request.POST.get('style_name')
        check_result = check_jwt(request.COOKIES.get('access_token'), True)

        if type(check_result) != type(True):
            return redirect("/admin/login")

        style = models.Style.objects.filter(style_id=_id)
        if style is not None:
            style.update(style_name=new_name)
            return redirect("/admin/styles")
        else:
            return redirect("/admin/styles?error=Такой стиль не существует", )
    return redirect("/admin/styles?error=Неверный метод запроса", )

'''
API v1
'''

@csrf_exempt
def api_add_style(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    form = StyleForm(request.POST)
    if not form.is_valid():
        return HttpResponse(status=400)

    style = models.Style.objects.filter(style_name=form.cleaned_data["style_name"]).first()
    if style is not None:
        return HttpResponse(status=400)

    models.Style.objects.create(style_name=form.cleaned_data["style_name"])
    return HttpResponse(status=200)


@csrf_exempt
def api_edit_style(request, _id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    new_name = request.POST.get('style_name')
    if not new_name:
        return HttpResponse(status=400)

    style = models.Style.objects.filter(style_id=_id)
    if not style.exists():
        return HttpResponseNotFound()

    style.update(style_name=new_name)
    return HttpResponse(status=200)


@csrf_exempt
def api_delete_style(request, _id: int):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    style = models.Style.objects.filter(style_id=_id)
    if style.exists():
        style.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound()


@csrf_exempt
def api_get_styles(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    styles = models.Style.objects.all()

    style_list = []
    for style_id, style_name in styles.values_list("style_id", "style_name"):
        style_list.append({"id": style_id, "name": style_name})

    return JsonResponse(data={"styles": style_list}, status=200)
