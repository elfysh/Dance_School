from django.shortcuts import render, redirect

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
