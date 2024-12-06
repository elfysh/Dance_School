import jwt
from django.shortcuts import render, redirect

from app import models
from app.views.helper import check_jwt
from sports_booking import settings


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
    dance_schools_dict = {dance_school.dance_school_id: dance_school for dance_school in dance_schools}

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
        content["events"].append(
            {
                "name": name,
                "date": date,
                "school_name": dance_schools_dict.get(dance_school_id).dance_school_name,
                "school_address": dance_schools_dict.get(dance_school_id).dance_school_address,
            }
        )
    for _id, name, time, hall_id, choreographer_id in classes.values_list("master_class_id", "master_class_name", "time", "hall_id", "choreographer_id"):
        content["classes"].append(
            {
                "id": _id,
                "name": name,
                "time": time,
                "hall": halls_dict.get(hall_id).hall_name,
                "school_name": dance_schools_dict.get(halls_dict.get(hall_id).dance_school_id.dance_school_id).dance_school_name,
                "school_address": dance_schools_dict.get(halls_dict.get(hall_id).dance_school_id.dance_school_id).dance_school_address,
                "choreographer": choreographers_dict.get(choreographer_id).choreographer_name,
                "is_subscribed": appointments_dict.get(user_id) is not None and _id in appointments_dict.get(user_id)
            }
        )

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
