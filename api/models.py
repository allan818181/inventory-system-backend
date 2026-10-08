from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Unaweza kuongeza fields zako hapa
    # phone = models.CharField(max_length=20, blank=True, null=True)

    # Added to match existing DB column (NOT NULL). Default False prevents NOT NULL insert errors.
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=0)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image_url = models.URLField(blank=True, null=True)  # frontend-only image placeholder
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StockMovement(models.Model):
    REASON_CHOICES = [
        ('add', 'Add'),
        ('remove', 'Remove'),
        ('sale', 'Sale'),
        ('restock', 'Restock'),
        ('adjust', 'Adjustment'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    change = models.IntegerField()  # positive to add, negative to remove
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    note = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}: {self.change} ({self.reason})"
