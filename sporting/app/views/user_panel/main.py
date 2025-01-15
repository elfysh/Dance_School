from datetime import datetime

import jwt
from django.shortcuts import render, redirect

from app import models
from app.models import DanceSchool
from app.views.helper import check_jwt
from sports_booking import settings
from app.forms.user_forms import FilterForm

def main(request):
    user_id = ""

    raw_token = request.COOKIES.get('access_token')
    if raw_token is None:
        return redirect("/user/login")
    try:
        payload = jwt.decode(raw_token, settings.SECRET_KEY_USER, algorithms=['HS256'])
        user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        print("Token is expired")
        return redirect("/user/login")
    except jwt.InvalidTokenError:
        print("Invalid token")
        return redirect("/user/login")

    from_date = datetime.strptime(request.GET.get("from_date"), "%Y-%m-%d").date() if request.GET.get("from_date") else None
    to_date = datetime.strptime(request.GET.get("to_date"), "%Y-%m-%d").date() if request.GET.get("to_date") else None
    styles = request.GET.getlist("styles") if request.GET.getlist("styles") else None

    classes_page = request.GET.get("classes_page") if request.GET.get("classes_page") else 1
    events_page = request.GET.get("events_page") if request.GET.get("events_page") else 1

    content = {
        "classes": [],
        "events": []
    }

    classes = (
        models
        .MasterClass
        .objects
        .all()
    )
    events = (
        models
        .Event
        .objects
        .all()
    )

    choreographers = (
        models
        .Choreographer
        .objects
        .all()
    )
    choreographers_dict = {choreographer.choreographer_id: choreographer for choreographer in choreographers}

    halls = (
        models
        .Hall
        .objects
        .all()
    )
    halls_dict = {hall.hall_id: hall for hall in halls}

    dance_schools = (
        models
        .DanceSchool
        .objects
        .all()
    )
    dance_schools_dict: dict[int: DanceSchool] = {dance_school.dance_school_id: dance_school for dance_school in dance_schools}

    appointments = (
        models
        .Appointment
        .objects
        .all()
    )
    # appointments_dict = {appointment.client_id.client_id: appointment.master_class_id.master_class_id for appointment in appointments}
    appointments_dict = {}
    for appointment in appointments:
        if appointment.client_id.client_id not in appointments_dict:
            appointments_dict[appointment.client_id.client_id] = []
        appointments_dict[appointment.client_id.client_id].append(appointment.master_class_id.master_class_id)
    print(user_id)
    print(appointments_dict)
    print(appointments_dict.get(user_id))

    for name, date, dance_school_id in events.values_list("event_name", "date", "dance_school_id"):
        if from_date is not None and from_date > date:
            continue
        if to_date is not None and to_date < date:
            continue
        content["events"].append(
            {
                "name": name,
                "date": date,
                "school_name": dance_schools_dict.get(dance_school_id).dance_school_name,
                "school_address": dance_schools_dict.get(dance_school_id).dance_school_address,
            }
        )
    for _id, name, time, hall_id, choreographer_id in classes.values_list("master_class_id", "master_class_name", "time", "hall_id", "choreographer_id"):
        if from_date is not None and from_date > time.date():
            continue
        if to_date is not None and to_date < time.date():
            continue
        if styles is not None and str(choreographers_dict.get(choreographer_id).style_id.style_id) not in styles:
            continue
        content["classes"].append(
            {
                "id": _id,
                "name": name,
                "time": time,
                "hall": halls_dict.get(hall_id).hall_name,
                "school_name": dance_schools_dict.get(halls_dict.get(hall_id).dance_school_id.dance_school_id).dance_school_name,
                "school_address": dance_schools_dict.get(halls_dict.get(hall_id).dance_school_id.dance_school_id).dance_school_address,
                "choreographer": choreographers_dict.get(choreographer_id).choreographer_name,
                "is_subscribed": appointments_dict.get(user_id) is not None and _id in appointments_dict.get(user_id),
                "style": choreographers_dict.get(choreographer_id).style_id.style_name
            }
        )

    content["classes_pages"] = [i for i in range(1, len(content["classes"]) // 3 + 2)]
    content["events_pages"] = [i for i in range(1, len(content["events"]) // 3 + 2)]

    content["classes"] = sorted(content["classes"], key=lambda x: x["time"])
    content["events"] = sorted(content["events"], key=lambda x: x["date"])

    content["classes"] = content["classes"][(int(classes_page) - 1) * 3:int(classes_page) * 3]
    content["events"] = content["events"][(int(events_page) - 1) * 3:int(events_page) * 3]



    styles = (
        models
        .Style
        .objects
        .all()
    )

    filter_form = FilterForm()
    filter_form.update_choices([(style.style_id, style.style_name) for style in styles])
    content["filter_form"] = filter_form

    return check_jwt(request, render(request, "user/user.html", content), settings.SECRET_KEY_USER, "/user/login")


def subscribe(request):
    if request.method != "POST":
        return redirect("/user?error=Неверный метод запроса")

    raw_token = request.COOKIES.get('access_token')
    if raw_token is None:
        return redirect("user/login")
    try:
        payload = jwt.decode(raw_token, settings.SECRET_KEY_USER, algorithms=['HS256'])
        user_id = payload["user_id"]
    except jwt.ExpiredSignatureError:
        print("Token is expired")
        return redirect("user/login")
    except jwt.InvalidTokenError:
        print("Invalid token")
        return redirect("user/login")

    class_id = request.POST.get("class_id")

    print(class_id)
    print(user_id)

    appointment = models.Appointment.objects.filter(client_id=user_id, master_class_id=class_id).first()

    print(appointment)

    if appointment is None:
        models.Appointment.objects.create(
            client_id=models.Client.objects.get(client_id=user_id),
            master_class_id=models.MasterClass.objects.get(master_class_id=class_id)
        )
    else:
        models.Appointment.objects.filter(client_id=user_id, master_class_id=class_id).delete()

    return redirect("/user")
