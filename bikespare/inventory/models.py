from django.db import models

# Create your models here.


from django.db import models
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Part(models.Model):
    part_number = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="parts")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="parts")
    description = models.TextField(blank=True)
    compatible_with = models.CharField(
        max_length=200,
        help_text="e.g. Honda Activa / Yamaha FZ"
    )
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return f"{self.part_number} – {self.name}"

    @property
    def in_stock(self):
        return self.quantity > 0

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "Out of stock"
        if self.quantity <= 5:
            return "Low stock"
        return "In stock"

    def get_absolute_url(self):
        return reverse("parts:part_detail", kwargs={"part_number": self.part_number})


class Enquiry(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=25)
    brand = models.CharField(max_length=80, blank=True)
    model = models.CharField(max_length=100, blank=True)
    part = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "enquiries"

    def __str__(self):
        return f"{self.name} – {self.part}"