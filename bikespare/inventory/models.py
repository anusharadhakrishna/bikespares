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

from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.urls import reverse


class Part(models.Model):

    part_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True
    )

    name = models.CharField(
        max_length=200
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="parts"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="parts"
    )

    description = models.TextField(
        blank=True
    )

    compatible_with = models.CharField(
        max_length=200,
        help_text="e.g. Honda Activa / Yamaha FZ"
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    # =========================
    # PRICING
    # =========================

    # This stores the calculated selling price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Selling Price",
        
    )

    # Original MRP
    mrp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="MRP"
    )

    # Discount percentage
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Discount (%)",
        help_text="Enter discount percentage, e.g. 10 for 10% OFF"
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return f"{self.part_number} – {self.name}"

    # =========================
    # CALCULATE PRICE
    # =========================

    def calculate_price(self):

        if self.mrp is None:
            return None

        mrp = Decimal(str(self.mrp))
        discount = Decimal(str(self.discount or 0))

        # No discount
        if discount <= 0:
            return mrp.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        # Discount amount
        discount_amount = (
            mrp * discount / Decimal("100")
        )

        # Final selling price
        selling_price = mrp - discount_amount

        return selling_price.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    # =========================
    # SAVE
    # =========================

    def save(self, *args, **kwargs):

        self.price = self.calculate_price()

        super().save(*args, **kwargs)

    # =========================
    # DISCOUNT HELPERS
    # =========================

    @property
    def has_discount(self):
        return (
            self.mrp is not None
            and self.discount > 0
        )

    @property
    def discount_amount(self):

        if self.mrp is None:
            return Decimal("0.00")

        amount = (
            Decimal(str(self.mrp))
            * Decimal(str(self.discount or 0))
            / Decimal("100")
        )

        return amount.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

    # =========================
    # STOCK
    # =========================

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

    # =========================
    # URL
    # =========================

    def get_absolute_url(self):

        return reverse(
            "parts:part_detail",
            kwargs={
                "part_number": self.part_number
            }
        )
# class Part(models.Model):
#     part_number = models.CharField(max_length=50, unique=True, db_index=True)
#     name = models.CharField(max_length=200)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="parts")
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="parts")
#     description = models.TextField(blank=True)
#     compatible_with = models.CharField(
#         max_length=200,
#         help_text="e.g. Honda Activa / Yamaha FZ"
#     )
#     quantity = models.PositiveIntegerField(default=0)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     mrp = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name="MRP"
#     )

#     discount = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         default=0,
#         verbose_name="Discount (%)"
#     )
#     is_featured = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-is_featured", "name"]

#     def __str__(self):
#         return f"{self.part_number} – {self.name}"

#     @property
#     def in_stock(self):
#         return self.quantity > 0

#     @property
#     def stock_status(self):
#         if self.quantity == 0:
#             return "Out of stock"
#         if self.quantity <= 5:
#             return "Low stock"
#         return "In stock"
    
    
#     @property
#     def has_discount(self):
#         return self.discount > 0

#     @property
#     def discount_amount(self):

#         if not self.mrp:
#             return 0

#         return self.mrp * self.discount / 100

#     def get_absolute_url(self):
#         return reverse("parts:part_detail", kwargs={"part_number": self.part_number})


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
    
    
    
from django.db import models


class Service(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="Service Title"
    )

    description = models.TextField(
        verbose_name="Description"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title