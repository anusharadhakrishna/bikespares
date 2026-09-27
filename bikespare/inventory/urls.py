from django.urls import path
from . import views


app_name = "parts"


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "parts/",
        views.home,
        name="parts_list"
    ),

    path(
        "parts/<str:part_number>/",
        views.part_detail,
        name="part_detail"
    ),

    path(
        "enquiries/",
        views.enquiry,
        name="enquiry"
    ),

    path(
        "enquiry-success/",
        views.enquiry_success,
        name="enquiry_success"
    ),
]