from django.contrib import admin
from .models import User, Supplier, Product, StockMovement

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'is_admin')
    search_fields = ('username', 'email')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_email', 'phone', 'created_at')
    search_fields = ('name', 'contact_email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'quantity', 'min_stock_level', 'supplier', 'updated_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'change', 'reason', 'created_by', 'created_at')
    search_fields = ('product__name', 'reason')
    list_filter = ('reason',)
