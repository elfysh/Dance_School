from django.shortcuts import render, redirect

from app import models
from app.forms.choreographer_forms import ChoreographerForm
from app.views.helper import check_jwt


def admin_choreographers(request):
    if request.method != "GET":
        return redirect("/admin/choreographers?error=Неверный метод запроса")

    error_message = request.GET.get("error")

    choreographers = models.Choreographer.objects.all()
    styles = models.Style.objects.all()
    styles_dict = {_id: name for _id, name in models.Style.objects.all().values_list("style_id", "style_name")}

    choreographer_form = ChoreographerForm()
    choreographer_form.update_choices([(style["style_id"], style["style_name"]) for style in styles.values("style_id", "style_name")])
    contents = {
        "choreographers": [],
        "error_message": error_message,
        "styles": [],
        "choreographer_form": choreographer_form
    }

    for choreographer_id, choreographer_name, style_id in choreographers.values_list("choreographer_id", "choreographer_name", "style_id"):
        contents["choreographers"].append(
            {
                "id": choreographer_id,
                "name": choreographer_name,
                "style": styles_dict[style_id]
            }
        )

    for style_id, style_name in styles.values_list("style_id", "style_name"):
        contents["styles"].append({"id": style_id, "name": style_name})

    contents["styles"].sort(key=lambda x: x["name"])
    contents["choreographers"].sort(key=lambda x: x["name"])

    return check_jwt(request, render(request, "admin/choreographer_list.html", contents))


def add_choreographer(request):
    if request.method == "POST":

        choreographer_name = request.POST.get('choreographer_name')
        style_id = request.POST.get('style')

        check_result = check_jwt(request.COOKIES.get('access_token'), True)
        if type(check_result) != type(True):
            return redirect("/admin/login")

        choreographer = models.Choreographer.objects.filter(choreographer_name=choreographer_name).first()
        if choreographer is None:
            models.Choreographer.objects.create(choreographer_name=choreographer_name, style_id=models.Style.objects.get(style_id=style_id))
            return redirect("/admin/choreographers")
        else:
            return redirect("/admin/choreographers?error=Такой хореограф уже существует")
    return redirect("/admin/choreographers?error=Неверный метод запроса")


def delete_choreographer(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/choreographers?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    choreographer = models.Choreographer.objects.filter(choreographer_id=_id)
    if choreographer.exists():
        choreographer.delete()
    else:
        return redirect("/admin/choreographers?error=Такого хореографа не существует")
    return redirect("/admin/choreographers")


def edit_choreographer(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/choreographers?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    new_name = request.POST.get('choreographer_name')
    new_style = request.POST.get('style')

    choreographer = models.Choreographer.objects.filter(choreographer_id=_id)
    if not choreographer.exists():
        return redirect("/admin/choreographers?error=Такого хореографа не существует")

    if new_name:
        choreographer.update(choreographer_name=new_name)
    if new_style:
        choreographer.update(style_id=models.Style.objects.get(style_id=int(new_style)))

    return redirect("/admin/choreographers")
