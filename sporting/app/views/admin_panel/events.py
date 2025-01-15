from django.http import HttpRequest
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from app import models
from app.forms.event_forms import EventForm, EditEventForm
from app.views.helper import check_jwt


def admin_event(request):
    if request.method != "GET":
        return redirect("/admin/events?error=Неверный метод запроса")

    error_message = request.GET.get("error")

    events = models.Event.objects.all()
    schools = models.DanceSchool.objects.all()

    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]
    school_dict = {school.dance_school_id: school.dance_school_name for school in schools}

    school_choices.sort(key=lambda x: x[1])

    add_form = EventForm()
    add_form.update_choices(school_choices)

    edit_form = EditEventForm()
    edit_form.update_choices(school_choices)

    contents = {
        "events": [],
        "error_message": error_message,
        "event_form": add_form,
        "edit_event_form": edit_form
    }

    for event_id, dance_school_id, name, date, description in events.values_list(
            "event_id",
            "dance_school_id",
            "event_name",
            "date",
            "description"
    ):
        contents["events"].append(
            {
                "id": event_id,
                "name": name,
                "date": date,
                "description": description,
                "school": school_dict[dance_school_id]
            }
        )

    contents["events"].sort(key=lambda x: x["name"])

    return check_jwt(request, render(request, "admin/event_list.html", contents))


def get_on_error_render(
        request: HttpRequest,
        message: str,
        event_form: EventForm = None,
        edit_event_form: EditEventForm = None
):
    events = models.Event.objects.all()
    schools = models.DanceSchool.objects.all()

    school_dict = {school.dance_school_id: school.dance_school_name for school in schools}

    events = [
        {
            "id": event_id,
            "name": name,
            "date": date,
            "description": description,
            "school": school_dict[dance_school_id]
        } for event_id, dance_school_id, name, date, description in events.values_list(
            "event_id",
            "dance_school_id",
            "event_name",
            "date",
            "description"
        )
    ]

    if event_form is None:
        event_form = EventForm()
    event_form.update_choices([(school.dance_school_id, school.dance_school_name) for school in schools])

    if edit_event_form is None:
        edit_event_form = EditEventForm()
    edit_event_form.update_choices([(school.dance_school_id, school.dance_school_name) for school in schools])

    events.sort(key=lambda x: x["name"])

    return render(
        request,
        "admin/event_list.html",
        {
            "error_message": message,
            "events": events,
            "event_form": event_form,
            "edit_event_form": edit_event_form
        }
    )


def add_event(request):
    if request.method != "POST":
        return redirect("/admin/events?error=Неверный метод запроса")

    schools = models.DanceSchool.objects.all()
    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]

    form = EventForm(request.POST)
    form.update_choices(school_choices)

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    if not form.is_valid():
        print(form.errors)
        return get_on_error_render(request=request, message="Неверные данные", event_form=form)

    event = models.Event.objects.filter(event_name=form.cleaned_data["name"]).first()

    if event is not None:
        return get_on_error_render(request=request, message="Такой ивент уже существует", event_form=form)

    models.Event.objects.create(
        dance_school_id=(models
                         .DanceSchool
                         .objects
                         .all()
                         .filter(dance_school_id=form.cleaned_data["dance_school"])
                         .first()
                         ),
        event_name=form.cleaned_data["name"],
        date=form.cleaned_data["date"],
        description=form.cleaned_data["description"]
    )
    return redirect("/admin/events")


def delete_event(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/events?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    event = models.Event.objects.filter(event_id=_id)
    if event.exists():
        event.delete()
        return redirect("/admin/events")
    else:
        return redirect("/admin/events?error=Такой школы не существует")


def edit_event(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/events?error=Неверный метод запроса")

    schools = models.DanceSchool.objects.all()
    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]

    form = EditEventForm(request.POST)
    form.update_choices(school_choices)

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    if not form.is_valid():
        return get_on_error_render(request=request, message="Неверные данные", edit_event_form=form)

    event = models.Event.objects.filter(event_id=_id)

    if event is None:
        return get_on_error_render(request=request, message="Такой ивент не существует", edit_event_form=form)

    new_name = form.cleaned_data["name"]
    new_date = form.cleaned_data["date"]
    new_description = form.cleaned_data["description"]
    new_school = form.cleaned_data["dance_school"]

    if new_name:
        event.update(event_name=new_name)
    if new_date:
        event.update(date=new_date)
    if new_description:
        event.update(description=new_description)
    if new_school:
        event.update(dance_school_id=models.DanceSchool.objects.filter(dance_school_id=new_school).first())

    return redirect("/admin/events")

'''
API v1
'''

@csrf_exempt
def api_add_event(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    form = EventForm(request.POST)
    schools = models.DanceSchool.objects.all()
    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]
    form.update_choices(school_choices)

    if not form.is_valid():
        return HttpResponse(status=400)

    event = models.Event.objects.filter(event_name=form.cleaned_data["name"]).first()
    if event is not None:
        return HttpResponse(status=400)

    models.Event.objects.create(
        dance_school_id=models.DanceSchool.objects.get(dance_school_id=form.cleaned_data["dance_school"]),
        event_name=form.cleaned_data["name"],
        date=form.cleaned_data["date"],
        description=form.cleaned_data["description"]
    )
    return HttpResponse(status=200)


@csrf_exempt
def api_edit_event(request, _id: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    form = EditEventForm(request.POST)
    schools = models.DanceSchool.objects.all()
    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]
    form.update_choices(school_choices)

    if not form.is_valid():
        return HttpResponse(status=400)

    event = models.Event.objects.filter(event_id=_id)
    if not event.exists():
        return HttpResponseNotFound()

    new_name = form.cleaned_data["name"]
    new_date = form.cleaned_data["date"]
    new_description = form.cleaned_data["description"]
    new_school = form.cleaned_data["dance_school"]

    if new_name:
        event.update(event_name=new_name)
    if new_date:
        event.update(date=new_date)
    if new_description:
        event.update(description=new_description)
    if new_school:
        event.update(dance_school_id=models.DanceSchool.objects.get(dance_school_id=new_school))

    return HttpResponse(status=200)


@csrf_exempt
def api_delete_event(request, _id: int):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    event = models.Event.objects.filter(event_id=_id)
    if event.exists():
        event.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound()


@csrf_exempt
def api_get_events(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    check_result = check_jwt(request.headers.get('Authorization').split(" ")[1], True)
    if type(check_result) != type(True):
        return HttpResponse(status=401)

    events = models.Event.objects.all()
    schools = models.DanceSchool.objects.all()
    school_dict = {school.dance_school_id: school.dance_school_name for school in schools}

    event_list = []
    for event_id, dance_school_id, name, date, description in events.values_list(
            "event_id",
            "dance_school_id",
            "event_name",
            "date",
            "description"
    ):
        event_list.append(
            {
                "id": event_id,
                "name": name,
                "date": date,
                "description": description,
                "school": school_dict[dance_school_id]
            }
        )

    return JsonResponse(data={"events": event_list}, status=200)
