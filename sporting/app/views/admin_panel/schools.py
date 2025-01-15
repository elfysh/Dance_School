import re

from django.http import HttpRequest
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from app import models
from app.forms.dance_school_forms import DanceSchoolForm, EditDanceSchoolForm
from app.views.helper import check_jwt


def admin_schools(request):
    if request.method != "GET":
        return redirect("/admin/schools?error=Неверный метод запроса")

    error_message = request.GET.get("error")

    schools = models.DanceSchool.objects.all()

    contents = {
        "schools": [],
        "error_message": error_message,
        "school_form": DanceSchoolForm(),
        "edit_school_form": EditDanceSchoolForm()
    }

    for school_id, name, address, phone in schools.values_list(
            "dance_school_id",
            "dance_school_name",
            "dance_school_address",
            "phone_number"
    ):
        contents["schools"].append(
            {
                "id": school_id,
                "name": name,
                "address": address,
                "phone": phone
            }
        )

    contents["schools"].sort(key=lambda x: x["name"])

    return check_jwt(request, render(request, "admin/dance_school_list.html", contents))


def get_on_error_render(
        request: HttpRequest,
        message: str,
        school_form: DanceSchoolForm = DanceSchoolForm(),
        edit_school_form: EditDanceSchoolForm = EditDanceSchoolForm()
):
    schools = [
        {
            "id": _id,
            "name": name,
            "address": address,
            "phone": phone
        } for _id, name, address, phone in models.DanceSchool.objects.all().values_list(
            "dance_school_id",
            "dance_school_name",
            "dance_school_address",
            "phone_number"
        )
    ]

    return render(
        request,
        "admin/dance_school_list.html",
        {
            "error_message": message,
            "schools": schools,
            "school_form": school_form,
            "edit_school_form": edit_school_form
        }
    )


def add_school(request):
    if request.method != "POST":
        return redirect("/admin/schools?error=Неверный метод запроса")

    form = DanceSchoolForm(request.POST)

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    if not form.is_valid():
        return get_on_error_render(request=request, message="Неверные данные", school_form=form)

    phone = form.cleaned_data["phone"]
    if not (
            re.match(r"^\+\d{1,3} ?\d{3} ?\d{3} ?\d{2} ?\d{2}$", phone) or
            re.match(r"^8 ?\d{3} ?\d{3} ?\d{2} ?\d{2}$", phone) or
            re.match(r"^\+\d{1,3} ?\(\d{3}\) ?\d{3}-\d{2}-\d{2}$", phone) or
            re.match(r"^8 ?\(\d{3}\) ?\d{3}-\d{2}-\d{2}$", phone) or
            re.match(r"^\d{3} ?\d{3} ?\d{2} ?\d{2}$", phone)
    ):
        return get_on_error_render(request=request, message="Неверный формат номера телефона", edit_school_form=form)

    school = models.DanceSchool.objects.filter(dance_school_name=form.cleaned_data["name"]).first()

    if school is not None:
        return get_on_error_render(request=request, message="Такая школа уже существует", school_form=form)

    models.DanceSchool.objects.create(
        dance_school_name=form.cleaned_data["name"],
        dance_school_address=form.cleaned_data["address"],
        phone_number=form.cleaned_data["phone"]
    )
    return redirect("/admin/schools")


def edit_school(request, _id):
    if request.method != "POST":
        return redirect("/admin/schools?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    form = EditDanceSchoolForm(request.POST)

    if not form.is_valid():
        return get_on_error_render(request=request, message="Неверные данные", edit_school_form=form)

    new_name = form.cleaned_data["name"]
    new_address = form.cleaned_data["address"]
    new_phone = form.cleaned_data["phone"].strip()

    school = models.DanceSchool.objects.filter(dance_school_id=_id)

    if school is None:
        return get_on_error_render(request=request, message="Такой школы не существует", edit_school_form=form)

    if new_name != "":
        school.update(dance_school_name=new_name)

    if new_address != "":
        school.update(dance_school_address=new_address)

    if new_phone != "":
        if not (
                re.match(r"^\+\d{1,3} ?\d{3} ?\d{3} ?\d{2} ?\d{2}$", new_phone) or
                re.match(r"^8 ?\d{3} ?\d{3} ?\d{2} ?\d{2}$", new_phone) or
                re.match(r"^\+\d{1,3} ?\(\d{3}\) ?\d{3}-\d{2}-\d{2}$", new_phone) or
                re.match(r"^8 ?\(\d{3}\) ?\d{3}-\d{2}-\d{2}$", new_phone) or
                re.match(r"^\d{3} ?\d{3} ?\d{2} ?\d{2}$", new_phone)
        ):
            return get_on_error_render(request=request, message="Неверный формат номера телефона", edit_school_form=form)
        else:
            school.update(phone_number=new_phone)

    return redirect("/admin/schools")


def delete_school(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/schools?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    school = models.DanceSchool.objects.filter(dance_school_id=_id)
    if school.exists():
        school.delete()
        return redirect("/admin/schools")
    else:
        return redirect("/admin/schools?error=Такой школы не существует")

'''
API v1
'''


@csrf_exempt
def api_add_school(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    form = DanceSchoolForm(request.POST)
    if not form.is_valid():
        return HttpResponse(status=400)

    school = models.DanceSchool.objects.filter(dance_school_name=form.cleaned_data["name"]).first()
    if school is not None:
        return HttpResponse(status=400)

    models.DanceSchool.objects.create(
        dance_school_name=form.cleaned_data["name"],
        dance_school_address=form.cleaned_data["address"],
        phone_number=form.cleaned_data["phone"]
    )
    return HttpResponse(status=200)


@csrf_exempt
def api_edit_school(request, _id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    form = EditDanceSchoolForm(request.POST)
    if not form.is_valid():
        return HttpResponse(status=400)

    school = models.DanceSchool.objects.filter(dance_school_id=_id)
    if not school.exists():
        return HttpResponseNotFound()

    new_name = form.cleaned_data["name"]
    new_address = form.cleaned_data["address"]
    new_phone = form.cleaned_data["phone"]

    if new_name:
        school.update(dance_school_name=new_name)
    if new_address:
        school.update(dance_school_address=new_address)
    if new_phone:
        school.update(phone_number=new_phone)

    return HttpResponse(status=200)


@csrf_exempt
def api_delete_school(request, _id: int):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    school = models.DanceSchool.objects.filter(dance_school_id=_id)
    if school.exists():
        school.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound()


@csrf_exempt
def api_get_schools(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    schools = models.DanceSchool.objects.all()

    school_list = []
    for school_id, name, address, phone in schools.values_list(
            "dance_school_id",
            "dance_school_name",
            "dance_school_address",
            "phone_number"
    ):
        school_list.append(
            {
                "id": school_id,
                "name": name,
                "address": address,
                "phone": phone
            }
        )

    return JsonResponse(data={"schools": school_list}, status=200)
