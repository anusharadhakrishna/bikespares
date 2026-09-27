from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import Part, Brand, Category
from .forms import EnquiryForm


def home(request):
    q = request.GET.get("q", "").strip()
    brand_slug = request.GET.get("brand", "").strip()
    category_slug = request.GET.get("category", "").strip()

    parts = (
        Part.objects
        .filter(is_active=True)
        .select_related("brand", "category")
    )

    # Search
    if q:
        parts = parts.filter(
            Q(name__icontains=q)
            | Q(part_number__icontains=q)
            | Q(compatible_with__icontains=q)
            | Q(description__icontains=q)
            | Q(brand__name__icontains=q)
            | Q(category__name__icontains=q)
        )

    # Brand filter
    if brand_slug:
        parts = parts.filter(
            brand__slug=brand_slug
        )

    # Category filter
    if category_slug:
        parts = parts.filter(
            category__slug=category_slug
        )

    # Featured products
    featured_parts = parts.filter(
        is_featured=True
    )[:6]

    # If no featured products match the filter,
    # show normal matching products
    if not featured_parts.exists():
        featured_parts = parts[:6]

    brands = Brand.objects.all()
    categories = Category.objects.all()

    enquiry_form = EnquiryForm()

    context = {
        "featured_parts": featured_parts,
        "brands": brands,
        "categories": categories,

        "search_q": q,
        "selected_brand": brand_slug,
        "selected_category": category_slug,

        "total_found": parts.count(),

        "enquiry_form": enquiry_form,
    }

    return render(
        request,
        "home.html",
        context
    )


def enquiry(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Enquiry sent successfully. We’ll get back to you soon."
            )

            return redirect(
                "parts:enquiry_success"
            )

    else:
        form = EnquiryForm()

    # IMPORTANT:
    # If validation fails, render the same homepage
    # with all dynamic data still available.

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

    featured_parts = parts.filter(
        is_featured=True
    )[:6]

    if not featured_parts.exists():
        featured_parts = parts[:6]

    context = {
        "featured_parts": featured_parts,
        "brands": Brand.objects.all(),
        "categories": Category.objects.all(),

        "search_q": q,
        "selected_brand": brand_slug,
        "selected_category": category_slug,

        "total_found": parts.count(),

        "enquiry_form": form,
    }

    return render(
        request,
        "parts/home.html",
        context
    )


def enquiry_success(request):
    return render(
        request,
        "parts/enquiry_success.html"
    )


def part_detail(request, part_number):
    part = get_object_or_404(
        Part,
        part_number=part_number,
        is_active=True
    )

    return render(
        request,
        "detail.html",
        {
            "part": part
        }
    )