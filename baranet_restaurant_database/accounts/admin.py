from django.contrib import admin
from .models import Product, CartItem, Category, Order, OrderItem


# Ürünleri Admin Paneline Ekle
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')  # Görüntülenecek alanlar
    search_fields = ('name', 'description')  # Arama yapılacak alanlar


# Sepet Öğelerini Admin Paneline Ekle
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')  # Görüntülenecek alanlar
    search_fields = ('user__username', 'product__name')  # Arama yapılacak alanlar


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address')
    search_fields = ('user__username', 'address')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__name',)