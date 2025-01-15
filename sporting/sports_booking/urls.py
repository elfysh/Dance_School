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

api_choreographers = [
    path("edit/<int:_id>", choreographers.api_edit_choreographer, name='api_edit_choreographer'),
    path("delete/<int:_id>", choreographers.api_delete_choreographer, name='api_delete_choreographer'),
    path("add", choreographers.api_add_choreographer, name='api_add_choreographer'),
    path("", choreographers.api_get_choreographers, name='api_get_choreographers'),
]

api_halls = [
    path("edit/<int:_id>", halls.api_edit_hall, name='api_edit_hall'),
    path("delete/<int:_id>", halls.api_delete_hall, name='api_delete_hall'),
    path("add", halls.api_add_hall, name='api_add_hall'),
    path("", halls.api_get_halls, name='api_get_halls'),
]

api_schools = [
    path("edit/<int:_id>", schools.api_edit_school, name='api_edit_school'),
    path("delete/<int:_id>", schools.api_delete_school, name='api_delete_school'),
    path("add", schools.api_add_school, name='api_add_school'),
    path("", schools.api_get_schools, name='api_get_schools'),
]

api_styles = [
    path("edit/<int:_id>", styles.api_edit_style, name='api_edit_style'),
    path("delete/<int:_id>", styles.api_delete_style, name='api_delete_style'),
    path("add", styles.api_add_style, name='api_add_style'),
    path("", styles.api_get_styles, name='api_get_styles'),
]

api_events = [
    path("edit/<int:_id>", events.api_edit_event, name='api_edit_event'),
    path("delete/<int:_id>", events.api_delete_event, name='api_delete_event'),
    path("add", events.api_add_event, name='api_add_event'),
    path("", events.api_get_events, name='api_get_events'),
]

api_classes = [
    path("edit/<int:_id>", classes.api_edit_class, name='api_edit_class'),
    path("delete/<int:_id>", classes.api_delete_class, name='api_delete_class'),
    path("add", classes.api_add_class, name='api_add_class'),
    path("", classes.api_get_classes, name='api_get_classes'),
]

api_v1 = [
    path("admin/login", general.api_admin_login, name="api_admin_login"),
    path("choreographers/", include(api_choreographers)),
    path("halls/", include(api_halls)),
    path("schools/", include(api_schools)),
    path("styles/", include(api_styles)),
    path("events/", include(api_events)),
    path("classes/", include(api_classes)),
]

urlpatterns = [
    path("admin/", include(admin_patterns)),
    path("user/", include(user_patterns)),
    path("", lambda request: render(request, "index.html")),
    path("api/v1/", include(api_v1)),
]
