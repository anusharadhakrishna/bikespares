from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Brand, Category, Part, Enquiry


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = (
        "part_number", "name", "brand", "category",
        "quantity", "stock_status", "is_featured", "is_active"
    )
    list_filter = ("brand", "category", "is_featured", "is_active")
    search_fields = ("part_number", "name", "compatible_with")
    list_editable = ("quantity", "is_featured", "is_active")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "part", "created_at", "is_handled")
    list_filter = ("is_handled", "created_at")
    search_fields = ("name", "phone", "part", "brand", "model")
    list_editable = ("is_handled",)