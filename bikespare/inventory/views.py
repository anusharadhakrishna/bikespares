# from django.shortcuts import render, redirect, get_object_or_404
# from django.db.models import Q
# from django.contrib import messages

# from .models import Part, Brand, Category
# from .forms import EnquiryForm

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import Part, Brand, Category,Service
from .forms import EnquiryForm


# =========================================================
# HOME PAGE
# =========================================================

def home(request):
    
    services = Service.objects.filter(
        is_active=True
    ).order_by("order", "id")

    # Show only 6 products on homepage
    featured_parts = (
        Part.objects
        .filter(
            is_active=True,
            is_featured=True
        )
        .select_related(
            "brand",
            "category"
        )[:6]
    )

    # If there are less than 6 featured products,
    # fill remaining spaces with normal active products.
    if featured_parts.count() < 6:

        featured_ids = featured_parts.values_list(
            "id",
            flat=True
        )

        remaining_parts = (
            Part.objects
            .filter(is_active=True)
            .exclude(id__in=featured_ids)
            .select_related(
                "brand",
                "category"
            )
        )

        featured_parts = list(featured_parts) + list(
            remaining_parts[:6 - len(featured_parts)]
        )

    brands = Brand.objects.all()

    categories = Category.objects.all()

    enquiry_form = EnquiryForm()

    context = {
        "services": services,
        "featured_parts": featured_parts,
        "brands": brands,
        "categories": categories,
        "enquiry_form": enquiry_form,
    }

    return render(
        request,
        "home.html",
        context
    )


# =========================================================
# PARTS LISTING PAGE
# =========================================================


from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q


def parts_list(request):

    q = request.GET.get("q", "").strip()
    brand_slug = request.GET.get("brand", "").strip()
    category_slug = request.GET.get("category", "").strip()

    parts = (
        Part.objects
        .filter(is_active=True)
        .select_related("brand", "category")
    )

    if q:
        parts = parts.filter(
            Q(name__icontains=q)
            | Q(part_number__icontains=q)
            | Q(compatible_with__icontains=q)
            | Q(description__icontains=q)
            | Q(brand__name__icontains=q)
            | Q(category__name__icontains=q)
        )

    if brand_slug:
        parts = parts.filter(
            brand__slug=brand_slug
        )

    if category_slug:
        parts = parts.filter(
            category__slug=category_slug
        )

    # 9 products per load
    paginator = Paginator(parts, 9)

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)

    context = {
        "parts": page_obj,
        "page_obj": page_obj,
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),
        "search_q": q,
        "selected_brand": brand_slug,
        "selected_category": category_slug,
        "total_found": paginator.count,
    }

    return render(
        request,
        "parts_list.html",
        context
    )
# def parts_list(request):

#     q = request.GET.get(
#         "q",
#         ""
#     ).strip()

#     brand_slug = request.GET.get(
#         "brand",
#         ""
#     ).strip()

#     category_slug = request.GET.get(
#         "category",
#         ""
#     ).strip()

#     parts = (
#         Part.objects
#         .filter(is_active=True)
#         .select_related(
#             "brand",
#             "category"
#         )
#     )

#     # -----------------------------------------------------
#     # SEARCH
#     # -----------------------------------------------------

#     if q:

#         parts = parts.filter(
#             Q(name__icontains=q)
#             |
#             Q(part_number__icontains=q)
#             |
#             Q(compatible_with__icontains=q)
#             |
#             Q(description__icontains=q)
#             |
#             Q(brand__name__icontains=q)
#             |
#             Q(category__name__icontains=q)
#         )

#     # -----------------------------------------------------
#     # BRAND FILTER
#     # -----------------------------------------------------

#     if brand_slug:

#         parts = parts.filter(
#             brand__slug=brand_slug
#         )

#     # -----------------------------------------------------
#     # CATEGORY FILTER
#     # -----------------------------------------------------

#     if category_slug:

#         parts = parts.filter(
#             category__slug=category_slug
#         )

#     context = {
#         "parts": parts,

#         "brands": Brand.objects.all(),

#         "categories": Category.objects.all(),

#         "search_q": q,

#         "selected_brand": brand_slug,

#         "selected_category": category_slug,

#         "total_found": parts.count(),
#     }

#     return render(
#         request,
#         "parts_list.html",
#         context
#     )


# =========================================================
# ENQUIRY
# =========================================================

# def enquiry(request):

#     if request.method == "POST":

#         form = EnquiryForm(
#             request.POST
#         )

#         if form.is_valid():

#             form.save()

#             messages.success(
#                 request,
#                 "Enquiry sent successfully. We’ll get back to you soon."
#             )

#             return redirect(
#                 "parts:enquiry_success"
#             )

#     else:

#         form = EnquiryForm()

#     # -----------------------------------------------------
#     # IF VALIDATION FAILS
#     # -----------------------------------------------------

#     featured_parts = (
#         Part.objects
#         .filter(
#             is_active=True,
#             is_featured=True
#         )
#         .select_related(
#             "brand",
#             "category"
#         )[:6]
#     )

#     if featured_parts.count() < 6:

#         featured_ids = featured_parts.values_list(
#             "id",
#             flat=True
#         )

#         remaining_parts = (
#             Part.objects
#             .filter(is_active=True)
#             .exclude(id__in=featured_ids)
#             .select_related(
#                 "brand",
#                 "category"
#             )
#         )

#         featured_parts = list(featured_parts) + list(
#             remaining_parts[:6 - len(featured_parts)]
#         )

#     context = {
#         "featured_parts": featured_parts,

#         "brands": Brand.objects.all(),

#         "categories": Category.objects.all(),

#         "enquiry_form": form,
#     }

#     return render(
#         request,
#         "home.html",
#         context
#     )

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import Part, Brand, Category
from .forms import EnquiryForm


def enquiry(request):

    if request.method == "POST":

        form = EnquiryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your enquiry has been sent successfully. We’ll get back to you soon."
            )

            return redirect(
                "parts:home"
            )

    else:
        form = EnquiryForm()

    # Homepage data
    featured_parts = (
        Part.objects
        .filter(
            is_active=True,
            is_featured=True
        )
        .select_related(
            "brand",
            "category"
        )[:6]
    )

    # Fill remaining products if less than 6
    if featured_parts.count() < 6:

        featured_ids = featured_parts.values_list(
            "id",
            flat=True
        )

        remaining_parts = (
            Part.objects
            .filter(is_active=True)
            .exclude(id__in=featured_ids)
            .select_related(
                "brand",
                "category"
            )
        )

        featured_parts = list(featured_parts) + list(
            remaining_parts[:6 - len(featured_parts)]
        )

    context = {
        "featured_parts": featured_parts,
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),
        "enquiry_form": form,
    }

    return render(
        request,
        "home.html",
        context
    )
# =========================================================
# ENQUIRY SUCCESS
# =========================================================

def enquiry_success(request):

    return render(
        request,
        "enquiry_success.html"
    )


# =========================================================
# PART DETAIL
# =========================================================
# def part_detail(request, part_number):
#     part = get_object_or_404(
#         Part.objects.select_related(
#             "brand",
#             "category"
#         ),
#         part_number=part_number,
#         is_active=True
#     )

#     # Related products:
#     # Same category OR same brand
#     related_parts = (
#         Part.objects
#         .filter(is_active=True)
#         .filter(
#             Q(category=part.category) |
#             Q(brand=part.brand)
#         )
#         .exclude(id=part.id)
#         .select_related("brand", "category")
#         .order_by("-is_featured", "name")[:4]
#     )

#     return render(
#         request,
#         "detail.html",
#         {
#             "part": part,
#             "related_parts": related_parts,
#         }
#     )


from django.shortcuts import get_object_or_404, render

from inventory.models import Part


def part_detail(request, part_number):

    part = get_object_or_404(
        Part.objects
        .filter(is_active=True)
        .select_related(
            "brand",
            "category",
        ),
        part_number=part_number,
    )

    related_parts = (
        Part.objects
        .filter(
            is_active=True,
            category=part.category,
        )
        .exclude(pk=part.pk)
        .select_related(
            "brand",
            "category",
        )
        .order_by(
            "-is_featured",
            "-created_at",
        )[:4]
    )

    context = {
        "part": part,
        "related_parts": related_parts,
    }

    return render(
        request,
        "detail.html",
        context,
    )
    
    
    
from django.http import JsonResponse
    
# =========================================================
# SEARCH SUGGESTIONS
# =========================================================

# def search_suggestions(request):

#     q = request.GET.get(
#         "q",
#         ""
#     ).strip()

#     if len(q) < 1:

#         return JsonResponse(
#             {
#                 "results": []
#             }
#         )


#     parts = (
#         Part.objects
#         .filter(
#             is_active=True
#         )
#         .filter(
#             Q(name__icontains=q)
#             |
#             Q(part_number__icontains=q)
#             |
#             Q(brand__name__icontains=q)
#             |
#             Q(category__name__icontains=q)
#             |
#             Q(compatible_with__icontains=q)
#         )
#         .select_related(
#             "brand",
#             "category"
#         )[:8]
#     )


#     results = []

#     for part in parts:

#         results.append({

#             "name": part.name,

#             "part_number": part.part_number,

#             "brand": part.brand.name,

#             "category": part.category.name,

#             "url": part.get_absolute_url(),

#         })


#     return JsonResponse(
#         {
#             "results": results
#         }
#     )

def search_suggestions(request):
    q = request.GET.get("q", "").strip()

    if len(q) < 1:
        return JsonResponse({"results": []})

    parts = (
        Part.objects
        .filter(is_active=True)
        .filter(
            Q(name__icontains=q)
            | Q(part_number__icontains=q)
            | Q(brand__name__icontains=q)
            | Q(category__name__icontains=q)
            | Q(compatible_with__icontains=q)
        )
        .select_related("brand", "category")[:6]   # ← 6 results
    )

    results = []

    for part in parts:
        results.append({
            "name": part.name,
            "part_number": part.part_number,
            "brand": part.brand.name,
            "category": part.category.name,
            "compatible_with": part.compatible_with,
            "url": part.get_absolute_url(),
        })

    return JsonResponse({
        "results": results
    })
    
   