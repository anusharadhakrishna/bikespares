from django.urls import path

from . import views


app_name = "dashboard"


urlpatterns = [
    path("login/", views.admin_login_view, name="admin_login"),
    path("logout/", views.admin_logout_view, name="admin_logout"),
    # =========================================================
    # DASHBOARD
    # =========================================================

    path(
        "",
        views.admin_dashboard,
        name="admin_dashboard",
    ),


    # =========================================================
    # PART CRUD
    # =========================================================

    path(
        "parts/",
        views.part_list_view,
        name="part_list",
    ),
    
    path(
        "parts/import/",
        views.part_import_view,
        name="part_import"
    ),

    path(
        "parts/add/",
        views.part_create_view,
        name="part_create",
    ),

    path(
        "parts/<int:pk>/edit/",
        views.part_update_view,
        name="part_update",
    ),

    path(
        "parts/<int:pk>/delete/",
        views.part_delete_view,
        name="part_delete",
    ),


    # =========================================================
    # BRAND CRUD
    # =========================================================

    path(
        "brands/",
        views.brand_list_view,
        name="brand_list",
    ),

    path(
        "brands/add/",
        views.brand_create_view,
        name="brand_create",
    ),

    path(
        "brands/<int:pk>/edit/",
        views.brand_update_view,
        name="brand_update",
    ),

    path(
        "brands/<int:pk>/delete/",
        views.brand_delete_view,
        name="brand_delete",
    ),


    # =========================================================
    # CATEGORY CRUD
    # =========================================================

    path(
        "categories/",
        views.category_list_view,
        name="category_list",
    ),

    path(
        "categories/add/",
        views.category_create_view,
        name="category_create",
    ),

    path(
        "categories/<int:pk>/edit/",
        views.category_update_view,
        name="category_update",
    ),

    path(
        "categories/<int:pk>/delete/",
        views.category_delete_view,
        name="category_delete",
    ),


    # =========================================================
    # ENQUIRIES
    # =========================================================

    path(
        "enquiries/",
        views.enquiry_list_view,
        name="enquiry_list"
    ),

    path(
        "enquiries/add/",
        views.enquiry_create_view,
        name="enquiry_create"
    ),

    path(
        "enquiries/<int:pk>/edit/",
        views.enquiry_update_view,
        name="enquiry_update"
    ),

    path(
        "enquiries/<int:pk>/delete/",
        views.enquiry_delete_view,
        name="enquiry_delete"
    ),

    path(
        "enquiries/<int:pk>/toggle/",
        views.toggle_enquiry_status,
        name="toggle_enquiry_status"
    ),

]