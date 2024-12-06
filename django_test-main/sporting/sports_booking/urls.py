from django.shortcuts import render
from django.urls import path, include

from app.views.admin_panel import choreographers, general, styles, schools, events, halls, classes
from app.views.user_panel import main, user_login

admin_patterns = [
    path("", general.admin),
    path("login", general.admin_login),

    ## STYLES
    path("styles", styles.admin_styles),
    path("add_style", styles.add_style),
    path("delete_style/<int:_id>", styles.delete_style),
    path("edit_style/<int:_id>", styles.edit_style),

    ## CHOREOGRAPHERS
    path("choreographers", choreographers.admin_choreographers),
    path("add_choreographer", choreographers.add_choreographer),
    path("delete_choreographer/<int:_id>", choreographers.delete_choreographer),
    path("edit_choreographer/<int:_id>", choreographers.edit_choreographer),

    ## SCHOOLS
    path("schools", schools.admin_schools),
    path("add_school", schools.add_school),
    path("delete_school/<int:_id>", schools.delete_school),
    path("edit_school/<int:_id>", schools.edit_school),

    ## EVENTS
    path("events", events.admin_event),
    path("add_event", events.add_event),
    path("delete_event/<int:_id>", events.delete_event),
    path("edit_event/<int:_id>", events.edit_event),

    ## HALLS
    path("halls", halls.admin_hall),
    path("add_hall", halls.add_hall),
    path("delete_hall/<int:_id>", halls.delete_hall),
    path("edit_hall/<int:_id>", halls.edit_hall),

    ## MASTER CLASSES
    path("classes", classes.admin_classes),
    path("add_class", classes.add_class),
    path("delete_class/<int:_id>", classes.delete_class),
    path("edit_class/<int:_id>", classes.edit_class)
]

user_patterns = [
    path("", main.main),
    path("login", user_login.user_login),
    path("signup", user_login.user_signup),
    path("subscribe", main.subscribe),
]

urlpatterns = [
    path("admin/", include(admin_patterns)),
    path("user/", include(user_patterns)),
    path("", lambda request: render(request, "index.html"))
]
