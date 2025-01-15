from datetime import datetime

from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from app import models
from app.forms.master_class_forms import MasterClassForm, EditMasterClassForm
from app.views.helper import check_jwt


def admin_classes(request):
    if request.method != "GET":
        return redirect("/admin/classes?error=Неверный метод запроса")

    error_message = request.GET.get("error")

    classes = models.MasterClass.objects.all()
    halls = models.Hall.objects.all()
    choreographers = models.Choreographer.objects.all()

    hall_choices = [(hall.hall_id, hall.hall_name) for hall in halls]
    hall_dict = {hall.hall_id: hall.hall_name for hall in halls}

    choreographer_choices = [(choreographer.choreographer_id, choreographer.choreographer_name) for choreographer in choreographers]
    choreographer_dict = {choreographer.choreographer_id: choreographer.choreographer_name for choreographer in choreographers}

    hall_choices.sort(key=lambda x: x[1])
    choreographer_choices.sort(key=lambda x: x[1])

    add_form = MasterClassForm()
    add_form.update_choices(hall_choices, choreographer_choices)

    edit_form = EditMasterClassForm()
    edit_form.update_choices(hall_choices, choreographer_choices)


    contents = {
        "classes": [],
        "error_message": error_message,
        "class_form": add_form,
        "edit_class_form": edit_form
    }

    for master_class_id, master_class_name, choreographer_id, hall_id, time in classes.values_list(
            "master_class_id",
            "master_class_name",
            "choreographer_id",
            "hall_id",
            "time"
    ):
        contents["classes"].append(
            {
                "id": master_class_id,
                "name": master_class_name,
                "hall": hall_dict[hall_id],
                "choreographer": choreographer_dict[choreographer_id],
                "time": time
            }
        )

    contents["classes"].sort(key=lambda x: x["name"])

    return check_jwt(request, render(request, "admin/master_class_list.html", contents))


def add_class(request):
    if request.method != "POST":
        return redirect("/admin/events?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    form = MasterClassForm(request.POST)

    halls = models.Hall.objects.all()
    choreographers = models.Choreographer.objects.all()

    hall_choices = [(hall.hall_id, hall.hall_name) for hall in halls]
    choreographer_choices = [(choreographer.choreographer_id, choreographer.choreographer_name) for choreographer in choreographers]

    form.update_choices(hall_choices, choreographer_choices)

    if not form.is_valid():
        print(form.errors)
        return redirect("/admin/classes?error=Неверные данные")



    hall_id = form.cleaned_data["hall"]
    choreographer_id = form.cleaned_data["choreographer"]
    date = form.cleaned_data["date"]
    time = form.cleaned_data["time"]
    name = form.cleaned_data["name"]

    datetime_comb = datetime.combine(date, time)
    print(name, choreographer_id, hall_id, time, date)

    m_class = models.MasterClass.objects.filter(
        master_class_name=name,
        hall_id=models.Hall.objects.all().filter(hall_id=hall_id).first(),
        time=datetime_comb
    ).first()

    if m_class is not None:
        return redirect("/admin/classes?error=Такой класс уже существует")


    models.MasterClass.objects.create(
        master_class_name=name,
        choreographer_id=models.Choreographer.objects.all().filter(choreographer_id=choreographer_id).first(),
        hall_id=models.Hall.objects.all().filter(hall_id=hall_id).first(),
        time=datetime_comb
    )

    return redirect("/admin/classes")


def delete_class(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/classes?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    m_class = models.MasterClass.objects.filter(master_class_id=_id)
    if m_class.exists():
        m_class.delete()
        return redirect("/admin/classes")
    else:
        return redirect("/admin/classes?error=Такого класса не существует")



def edit_class(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/classes?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    form = EditMasterClassForm(request.POST)

    halls = models.Hall.objects.all()
    choreographers = models.Choreographer.objects.all()

    hall_choices = [(hall.hall_id, hall.hall_name) for hall in halls]
    choreographer_choices = [(choreographer.choreographer_id, choreographer.choreographer_name) for choreographer in choreographers]

    form.update_choices(hall_choices, choreographer_choices)

    if not form.is_valid():
        print(form.errors)
        return redirect("/admin/classes?error=Неверные данные")

    m_class = models.MasterClass.objects.filter(master_class_id=_id)
    if m_class is None:
        return redirect("/admin/classes?error=Такого класса не существует")

    choreographer_id = form.cleaned_data["choreographer"]
    hall_id = form.cleaned_data["hall"]
    date = form.cleaned_data["date"]
    time = form.cleaned_data["time"]
    name = form.cleaned_data["name"]

    if name:
        m_class.update(master_class_name=name)

    if choreographer_id:
        m_class.update(choreographer_id=models.Choreographer.objects.all().filter(choreographer_id=choreographer_id).first())

    if hall_id:
        m_class.update(hall_id=models.Hall.objects.all().filter(hall_id=hall_id).first())

    if date and time:
        datetime_comb = datetime.combine(date, time)
        m_class.update(time=datetime_comb)
    elif date or time:
        return redirect("/admin/classes?error=Вы не можете изменить только год или время")

    return redirect("/admin/classes")

'''
API v1
'''

@csrf_exempt
def api_edit_class(request, _id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    form = EditMasterClassForm(request.POST)

    halls = models.Hall.objects.all()
    choreographers = models.Choreographer.objects.all()

    hall_choices = [(hall.hall_id, hall.hall_name) for hall in halls]
    choreographer_choices = [(choreographer.choreographer_id, choreographer.choreographer_name) for choreographer in choreographers]

    form.update_choices(hall_choices, choreographer_choices)

    if not form.is_valid():
        print(form.errors)
        return HttpResponse(status=400)

    m_class = models.MasterClass.objects.filter(master_class_id=_id)
    if m_class is None:
        return HttpResponseNotFound()

    choreographer_id = form.cleaned_data["choreographer"]
    hall_id = form.cleaned_data["hall"]
    date = form.cleaned_data["date"]
    time = form.cleaned_data["time"]
    name = form.cleaned_data["name"]

    if name:
        m_class.update(master_class_name=name)

    if choreographer_id:
        m_class.update(choreographer_id=models.Choreographer.objects.all().filter(choreographer_id=choreographer_id).first())

    if hall_id:
        m_class.update(hall_id=models.Hall.objects.all().filter(hall_id=hall_id).first())

    if date and time:
        datetime_comb = datetime.combine(date, time)
        m_class.update(time=datetime_comb)

    return HttpResponse(status=200)


@csrf_exempt
def api_delete_class(request, _id: int):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    m_class = models.MasterClass.objects.filter(master_class_id=_id)
    if m_class.exists():
        m_class.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound()


@csrf_exempt
def api_add_class(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    form = MasterClassForm(request.POST)

    halls = models.Hall.objects.all()
    choreographers = models.Choreographer.objects.all()

    hall_choices = [(hall.hall_id, hall.hall_name) for hall in halls]
    choreographer_choices = [(choreographer.choreographer_id, choreographer.choreographer_name) for choreographer in choreographers]

    form.update_choices(hall_choices, choreographer_choices)

    if not form.is_valid():
        print(form.errors)
        return HttpResponse(status=400)

    hall_id = form.cleaned_data["hall"]
    choreographer_id = form.cleaned_data["choreographer"]
    date = form.cleaned_data["date"]
    time = form.cleaned_data["time"]
    name = form.cleaned_data["name"]

    datetime_comb = datetime.combine(date, time)
    print(name, choreographer_id, hall_id, time, date)

    m_class = models.MasterClass.objects.filter(
        master_class_name=name,
        hall_id=models.Hall.objects.all().filter(hall_id=hall_id).first(),
        time=datetime_comb
    ).first()

    if m_class is not None:
        return HttpResponse(status=400)

    models.MasterClass.objects.create(
        master_class_name=name,
        choreographer_id=models.Choreographer.objects.all().filter(choreographer_id=choreographer_id).first(),
        hall_id=models.Hall.objects.all().filter(hall_id=hall_id).first(),
        time=datetime_comb
    )

    return HttpResponse(status=200)


@csrf_exempt
def api_get_classes(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    classes = models.MasterClass.objects.all()
    halls = models.Hall.objects.all()
    choreographers = models.Choreographer.objects.all()

    hall_dict = {hall.hall_id: hall.hall_name for hall in halls}
    choreographer_dict = {choreographer.choreographer_id: choreographer.choreographer_name for choreographer in choreographers}

    response = []

    for master_class_id, master_class_name, choreographer_id, hall_id, time in classes.values_list(
            "master_class_id",
            "master_class_name",
            "choreographer_id",
            "hall_id",
            "time"
    ):
        response.append(
            {
                "id": master_class_id,
                "name": master_class_name,
                "hall": hall_dict[hall_id],
                "choreographer": choreographer_dict[choreographer_id],
                "time": time
            }
        )

    return JsonResponse(data = {"classes": response}, status=200)
